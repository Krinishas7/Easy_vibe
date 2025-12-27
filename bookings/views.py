from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from events.models import Event
from payments.models import Payment
from .models import Booking, Ticket
from .forms import BookingForm
from .utils import generate_ticket_pdf, generate_qr_code, send_booking_confirmation_email, verify_ticket_qr
from .tasks import cancel_expired_booking

# --------------- LOCATION SECURITY IMPORTS ---------------
from .utils import get_ip_location, is_inside_nepal, gps_ip_match


import uuid
import json


# -------------------------------
# BOOKING CREATION
# -------------------------------
@login_required
@require_POST
def create_booking(request, slug):
    """Create a new booking for an event"""
    event = get_object_or_404(Event, slug=slug, status='published')

    # ----------------------------------------------------
    # LOCATION VALIDATION (GPS + IP HYBRID ALGORITHM)
    # ----------------------------------------------------
    user_ip = request.META.get("REMOTE_ADDR")

    # 1) IP GEOLOCATION
    ip_info = get_ip_location(user_ip)
    if not is_inside_nepal(ip_info):
        messages.error(request, "Ticket booking is only allowed inside Nepal.")
        return redirect('events:event_detail', slug=slug)

    # 2) GPS FROM FRONTEND (lat, lon)
    user_lat = request.POST.get("lat")
    user_lon = request.POST.get("lon")

    if not user_lat or not user_lon:
        messages.error(request, "Please enable location services to continue booking.")
        return redirect('events:event_detail', slug=slug)

    user_gps = {"lat": float(user_lat), "lon": float(user_lon)}

    # 3) GPS ↔ IP CROSS-CHECK (blocks VPN & GPS spoofing)
    if not gps_ip_match(user_gps, ip_info):
        messages.error(request, "Your GPS location does not match your network region. Disable VPN or proxy.")
        return redirect('events:event_detail', slug=slug)

    # ----------------------------------------------------
    # ORIGINAL BOOKING LOGIC CONTINUES BELOW
    # ----------------------------------------------------

    if not event.is_available:
        messages.error(request, 'This event is not available for booking.')
        return redirect('events:event_detail', slug=slug)

    form = BookingForm(request.POST, event=event)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        seat_type = form.cleaned_data['seat_type']

        # 1) Per-seat-type limit
        if seat_type.total_seats:
            already_booked = Booking.objects.filter(
                event=event,
                seat_type=seat_type,
                status__in=['pending', 'confirmed']
            ).aggregate(total=Sum('quantity'))['total'] or 0

            remaining_for_type = seat_type.total_seats - already_booked

            if remaining_for_type <= 0:
                messages.error(request, f'No seats left for {seat_type.name}.')
                return redirect('events:event_detail', slug=slug)

            if quantity > remaining_for_type:
                messages.error(request, f'Only {remaining_for_type} seats are left for {seat_type.name}.')
                return redirect('events:event_detail', slug=slug)

        # 2) Overall event availability
        if quantity > event.available_tickets:
            messages.error(request, f'Only {event.available_tickets} tickets are available.')
            return redirect('events:event_detail', slug=slug)

        try:
            with transaction.atomic():
                # Create booking
                booking = Booking.objects.create(
                    user=request.user,
                    event=event,
                    seat_type=seat_type,
                    quantity=quantity,
                    contact_name=form.cleaned_data['contact_name'],
                    contact_email=form.cleaned_data['contact_email'],
                    contact_phone=form.cleaned_data['contact_phone'],
                    status='pending'
                )

                # Update event tickets
                event.available_tickets -= quantity
                event.save()

                # Create payment record
                Payment.objects.create(
                    booking=booking,
                    amount=booking.total_amount,
                    payment_method='esewa',
                    status='pending'
                )

                # Auto-cancel after 5 minutes
                cancel_expired_booking.apply_async(
                    args=[str(booking.booking_id)],
                    countdown=300
                )

                messages.success(request, 'Booking created successfully! Please complete payment within 5 minutes.')
                return redirect('payments:initiate_payment', booking_id=booking.booking_id)

        except Exception:
            messages.error(request, 'An error occurred while creating your booking. Please try again.')
            return redirect('events:event_detail', slug=slug)

    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
        return redirect('events:event_detail', slug=slug)


# -------------------------------
# USER BOOKING VIEWS
# -------------------------------
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookings/my_bookings.html', {
        'page_obj': page_obj,
        'title': 'My Bookings'
    })


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking,
        'title': f'Booking {booking.booking_id}'
    })


# -------------------------------
# CANCEL BOOKING
# -------------------------------
@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

    if not booking.can_be_cancelled:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:booking_detail', booking_id=booking_id)

    try:
        with transaction.atomic():
            booking.status = 'cancelled'
            booking.save()

            # Restore tickets
            event = booking.event
            event.available_tickets += booking.quantity
            event.save()

            # Refund if exists
            try:
                payment = booking.payment
                payment.status = 'refunded'
                payment.save()
            except Payment.DoesNotExist:
                pass

            messages.success(request, 'Booking cancelled successfully.')

    except Exception:
        messages.error(request, 'An error occurred while cancelling your booking.')

    return redirect('bookings:booking_detail', booking_id=booking_id)


# -------------------------------
# DOWNLOAD TICKETS
# -------------------------------
@login_required
def download_tickets(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if booking.status != 'confirmed':
        messages.error(request, 'Tickets are only available for confirmed bookings.')
        return redirect('bookings:booking_detail', booking_id=booking_id)

    if not booking.tickets.exists():
        generate_tickets_for_booking(booking)

    try:
        pdf_buffer = generate_ticket_pdf(booking)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="tickets_{booking.booking_id}.pdf"'
        return response
    except Exception:
        messages.error(request, 'Error generating PDF. Please try again.')
        return redirect('bookings:booking_detail', booking_id=booking_id)


def generate_tickets_for_booking(booking):
    if booking.status != 'confirmed':
        return
    
    booking.tickets.all().delete()
    tickets = []
    for _ in range(booking.quantity):
        ticket = Ticket.objects.create(
            booking=booking,
            attendee_name=booking.contact_name,
            attendee_email=booking.contact_email
        )
        generate_qr_code(ticket)
        tickets.append(ticket)
    
    send_booking_confirmation_email(booking)
    return tickets


# -------------------------------
# QR SCANNER VIEWS
# -------------------------------
@login_required
def qr_scanner(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the scanner.')
        return redirect('events:home')
    
    return render(request, 'bookings/qr_scanner.html', {'title': 'QR Code Scanner'})


@login_required
def scanner_guide(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('events:home')
    
    return render(request, 'bookings/scanner_guide.html', {'title': 'QR Scanner Guide'})


# -------------------------------
# QR CODE VERIFICATION API
# -------------------------------
@login_required
@require_POST
def verify_ticket_api(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Unauthorized access'}, status=403)
    
    try:
        data = json.loads(request.body)
        qr_data = data.get('qr_data', '')
        
        if not qr_data:
            return JsonResponse({'success': False, 'error': 'No QR data provided'})
        
        is_valid, result = verify_ticket_qr(qr_data)
        
        if is_valid:
            ticket_info = result
            ticket = ticket_info['ticket']
            event = ticket_info['event']
            booking = ticket_info['booking']
            
            return JsonResponse({
                'success': True,
                'valid': True,
                'ticket': {
                    'ticket_id': str(ticket.ticket_id),
                    'attendee_name': ticket.attendee_name,
                    'attendee_email': ticket.attendee_email,
                    'is_used': ticket.is_used,
                    'used_at': ticket.used_at.isoformat() if ticket.used_at else None,
                },
                'event': {
                    'title': event.title,
                    'date': event.start_date.strftime('%B %d, %Y at %I:%M %p'),
                    'venue': event.venue,
                    'address': event.address,
                },
                'booking': {
                    'booking_id': str(booking.booking_id),
                    'contact_name': booking.contact_name,
                    'quantity': booking.quantity,
                    'status': booking.status,
                }
            })
        else:
            return JsonResponse({'success': True, 'valid': False, 'error': result})
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})


@login_required
@require_POST
def mark_ticket_used(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Unauthorized access'}, status=403)
    
    try:
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id', '')
        
        if not ticket_id:
            return JsonResponse({'success': False, 'error': 'No ticket ID provided'})
        
        ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
        
        if ticket.is_used:
            return JsonResponse({
                'success': False,
                'error': 'Ticket has already been used',
                'used_at': ticket.used_at.isoformat() if ticket.used_at else None
            })
        
        ticket.is_used = True
        ticket.used_at = timezone.now()
        ticket.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Ticket marked as used successfully',
            'used_at': ticket.used_at.isoformat()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})
