from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Event, Category, SeatType
from bookings.models import Booking
from payments.models import Payment


def home_view(request):
    featured_events = Event.objects.filter(
        status='published'
    ).order_by('-created_at')[:6]
    
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_events': featured_events,
        'categories': categories,
        'title': 'Home'
    }
    return render(request, 'events/home.html', context)


def event_list_view(request):
    events = Event.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    selected_category_name = None
    if category_id:
        events = events.filter(category_id=category_id)
        try:
            selected_category_name = Category.objects.get(id=category_id).name
        except Category.DoesNotExist:
            pass
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(venue__icontains=search_query)
        )
    
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'selected_category_name': selected_category_name,
        'search_query': search_query,
        'title': 'Events'
    }
    return render(request, 'events/event_list.html', context)


def event_detail_view(request, slug):
    event = get_object_or_404(Event, slug=slug, status='published')
    
    related_events = Event.objects.filter(
        category=event.category,
        status='published'
    ).exclude(id=event.id)[:4]

    seat_types = event.seat_types.filter(total_seats__gt=0)

    context = {
        'event': event,
        'related_events': related_events,
        'seat_types': seat_types,
        'title': event.title
    }
    return render(request, 'events/event_detail.html', context)



@login_required
def book_ticket_view(request, slug):
    event = get_object_or_404(Event, slug=slug, status='published')

    if request.method != "POST":
        return redirect("events:event_detail", slug=slug)

    seat_type_id = request.POST.get("seat_type")
    quantity = int(request.POST.get("quantity", 1))

    contact_name = request.POST.get("contact_name")
    contact_email = request.POST.get("contact_email")
    contact_phone = request.POST.get("contact_phone")


    if not event.allow_any_country:
        user_country = getattr(request.user.profile, "country", None)

        if not user_country or user_country.lower() != event.country.lower():
            messages.error(
                request,
                f"Booking restricted: This event is only available for users in {event.country}."
            )
            return redirect("events:event_detail", slug=slug)

    seat_type = get_object_or_404(SeatType, id=seat_type_id, event=event)

    if seat_type.seats_available < quantity:
        messages.error(request, "Not enough seats available for this seat type.")
        return redirect("events:event_detail", slug=slug)

    booking = Booking.objects.create(
        user=request.user,
        event=event,
        seat_type=seat_type,
        quantity=quantity,
        total_amount=seat_type.price * quantity,
        contact_name=contact_name,
        contact_email=contact_email,
        contact_phone=contact_phone,
        status="pending",
    )

    Payment.objects.create(
        booking=booking,
        amount=booking.total_amount,
        payment_method='esewa',
        status='pending'
    )

    return redirect("payments:initiate_payment", booking_id=booking.booking_id)



@login_required
def organizer_dashboard_view(request):
    events = Event.objects.filter(organizer=request.user)

    context = {
        "events": events,
        "title": "Organizer Dashboard",
    }
    return render(request, "events/organizer/dashboard.html", context)


# -------------------------------------
# MANAGE SPECIFIC EVENT
# -------------------------------------
@login_required
def organizer_event_manage_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.organizer != request.user:
        return HttpResponseForbidden("You are not allowed to manage this event.")

    seat_types = event.seat_types.all()
    bookings = event.bookings.filter(status="confirmed")

    context = {
        "event": event,
        "seat_types": seat_types,
        "bookings": bookings,
        "title": f"Manage {event.title}",
    }
    return render(request, "events/organizer/manage_event.html", context)


# -------------------------------------
# UPDATE SEAT TYPE
# -------------------------------------
@login_required
def organizer_update_seat_view(request, event_id, seat_id):
    event = get_object_or_404(Event, id=event_id)
    
    if event.organizer != request.user:
        return HttpResponseForbidden("You cannot edit seats for this event.")

    seat = get_object_or_404(SeatType, id=seat_id, event=event)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "increase":
            seat.total_seats += 1

        elif action == "decrease" and seat.total_seats > 0:
            if seat.total_seats > seat.tickets_sold:
                seat.total_seats -= 1
            else:
                messages.error(request, "Cannot reduce seats below the number already sold.")

        seat.save()
        messages.success(request, "Seat count updated successfully.")

    return redirect("events:organizer_event_manage", event_id=event.id)
