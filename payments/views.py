from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from bookings.models import Booking
from bookings.views import generate_tickets_for_booking
from .models import Payment
from .utils import generate_esewa_signature, verify_esewa_payment
import hashlib
import hmac
import json
import requests
import logging

logger = logging.getLogger(__name__)


@login_required
def initiate_payment(request, booking_id):
    """Initiate payment for a booking"""
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if booking.status != 'pending':
        messages.error(request, 'Payment can only be made for pending bookings.')
        return redirect('bookings:booking_detail', booking_id=booking_id)
    
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        messages.error(request, 'Payment record not found.')
        return redirect('bookings:booking_detail', booking_id=booking_id)
    
    # Prepare eSewa payment data
    esewa_data = {
        'amt': str(payment.amount),
        'pdc': '0',  # Delivery charge
        'psc': '0',  # Service charge
        'txAmt': '0',  # Tax amount
        'tAmt': str(payment.amount),  # Total amount
        'pid': str(booking.booking_id),  # Product ID (booking ID)
        'scd': settings.ESEWA_MERCHANT_ID,  # Service code (merchant ID)
        'su': settings.ESEWA_SUCCESS_URL,  # Success URL
        'fu': settings.ESEWA_FAILURE_URL,  # Failure URL
    }
    
    context = {
        'booking': booking,
        'payment': payment,
        'esewa_data': esewa_data,
        'esewa_url': 'https://rc.esewa.com.np/epay/main',  # Test URL
        'title': 'Payment'
    }
    
    return render(request, 'payments/initiate_payment.html', context)


def payment_success(request):
    """Handle successful payment from eSewa"""
    # Get parameters from eSewa
    oid = request.GET.get('oid')  # Our booking ID
    amt = request.GET.get('amt')
    refId = request.GET.get('refId')  # eSewa reference ID
    
    if not all([oid, amt, refId]):
        messages.error(request, 'Invalid payment response from eSewa.')
        return redirect('bookings:my_bookings')
    
    try:
        booking = get_object_or_404(Booking, booking_id=oid)
        
        # Verify payment with eSewa
        verification_result = verify_esewa_payment(oid, amt, refId)
        
        if verification_result.get('status') == 'success':
            # Payment verified successfully
            payment = booking.payment
            payment.mark_completed(
                transaction_id=refId,
                reference_id=refId
            )
            
            # Generate tickets for the booking
            generate_tickets_for_booking(booking)
            
            messages.success(request, 'Payment successful! Your booking has been confirmed.')
            return redirect('bookings:booking_detail', booking_id=booking.booking_id)
        else:
            # Payment verification failed
            payment = booking.payment
            payment.mark_failed()
            
            messages.error(request, 'Payment verification failed. Please contact support.')
            return redirect('bookings:booking_detail', booking_id=booking.booking_id)
            
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('bookings:my_bookings')
    except Exception as e:
        logger.error(f'Payment success handling error: {str(e)}')
        messages.error(request, 'An error occurred while processing your payment.')
        return redirect('bookings:my_bookings')


def payment_failure(request):
    """Handle failed payment from eSewa"""
    pid = request.GET.get('pid')  # Our booking ID
    
    if pid:
        try:
            booking = get_object_or_404(Booking, booking_id=pid)
            payment = booking.payment
            payment.mark_failed()
            
            messages.error(request, 'Payment failed or was cancelled. Please try again.')
            return redirect('bookings:booking_detail', booking_id=booking.booking_id)
            
        except Booking.DoesNotExist:
            pass
    
    messages.error(request, 'Payment failed or was cancelled.')
    return redirect('bookings:my_bookings')


@csrf_exempt
@require_POST
def esewa_webhook(request):
    """Handle eSewa webhook notifications"""
    try:
        # Parse the webhook data
        data = json.loads(request.body)
        
        booking_id = data.get('product_id')
        transaction_id = data.get('transaction_id')
        status = data.get('status')
        amount = data.get('amount')
        
        if not all([booking_id, transaction_id, status]):
            return HttpResponse('Invalid data', status=400)
        
        booking = Booking.objects.get(booking_id=booking_id)
        payment = booking.payment
        
        if status == 'COMPLETE':
            if payment.status == 'pending':
                payment.mark_completed(transaction_id=transaction_id)
                generate_tickets_for_booking(booking)
                logger.info(f'Payment completed via webhook: {booking_id}')
        elif status == 'FAILED':
            if payment.status == 'pending':
                payment.mark_failed()
                logger.info(f'Payment failed via webhook: {booking_id}')
        
        return HttpResponse('OK', status=200)
        
    except Exception as e:
        logger.error(f'Webhook processing error: {str(e)}')
        return HttpResponse('Error', status=500)


@login_required
def payment_status(request, booking_id):
    """Check payment status via AJAX"""
    try:
        booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
        payment = booking.payment
        
        return JsonResponse({
            'status': payment.status,
            'booking_status': booking.status,
            'message': f'Payment is {payment.get_status_display().lower()}'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Unable to check payment status'
        }, status=400)
