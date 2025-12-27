import qrcode
import io
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def generate_qr_code(ticket):
    """Generate QR code for a ticket"""
    # Create QR code data
    qr_data = f"TICKET:{ticket.ticket_id}|EVENT:{ticket.booking.event.slug}|BOOKING:{ticket.booking.booking_id}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Save to ticket model
    filename = f'qr_code_{ticket.ticket_id}.png'
    ticket.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)
    
    return ticket.qr_code


def generate_ticket_pdf(booking):
    """Generate PDF tickets for a booking"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0d6efd')
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#495057')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6
    )
    
    # Title
    story.append(Paragraph("EventBook - E-Ticket", title_style))
    story.append(Spacer(1, 20))
    
    # Event Information
    story.append(Paragraph("Event Information", header_style))
    
    event_data = [
        ['Event:', booking.event.title],
        ['Date & Time:', booking.event.start_date.strftime('%A, %B %d, %Y - %I:%M %p')],
        ['Venue:', booking.event.venue],
        ['Address:', booking.event.address],
        ['Category:', booking.event.category.name],
    ]
    
    event_table = Table(event_data, colWidths=[2*inch, 4*inch])
    event_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(event_table)
    story.append(Spacer(1, 20))
    
    # Booking Information
    story.append(Paragraph("Booking Information", header_style))
    
    booking_data = [
        ['Booking ID:', str(booking.booking_id)],
        ['Contact Name:', booking.contact_name],
        ['Contact Email:', booking.contact_email],
        ['Contact Phone:', booking.contact_phone],
        ['Seat Type:', booking.seat_type.name],
        ['Price per Ticket:', f'Rs. {booking.seat_type.price}'],
        ['Number of Tickets:', str(booking.quantity)],
        ['Booking Date:', booking.created_at.strftime('%B %d, %Y - %I:%M %p')],
        ['Total Amount:', f'Rs. {booking.total_amount}'],
    ]
    
    booking_table = Table(booking_data, colWidths=[2*inch, 4*inch])
    booking_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(booking_table)
    story.append(Spacer(1, 30))
    
    # Individual Tickets
    story.append(Paragraph("Your Tickets", header_style))
    
    for i, ticket in enumerate(booking.tickets.all(), 1):
        # Generate QR code if not exists
        if not ticket.qr_code:
            generate_qr_code(ticket)
        
        story.append(Paragraph(f"Ticket #{i}", ParagraphStyle(
            'TicketHeader',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=10,
            textColor=colors.HexColor('#28a745')
        )))
        
        # Ticket details and QR code side by side
        ticket_data = [
            ['Ticket ID:', str(ticket.ticket_id)],
            ['Attendee:', ticket.attendee_name],
            ['Seat Type:', booking.seat_type.name],
            ['Status:', 'Valid' if ticket.is_valid else 'Invalid'],
        ]
        
        ticket_table = Table(ticket_data, colWidths=[1.5*inch, 2.5*inch])
        ticket_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        # Create a table with ticket info and QR code
        if ticket.qr_code and os.path.exists(ticket.qr_code.path):
            qr_image = RLImage(ticket.qr_code.path, width=1.5*inch, height=1.5*inch)
            combined_data = [[ticket_table, qr_image]]
            combined_table = Table(combined_data, colWidths=[4*inch, 2*inch])
            combined_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(combined_table)
        else:
            story.append(ticket_table)
        
        story.append(Spacer(1, 20))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("Important Notes:", header_style))
    story.append(Paragraph("• Please bring this ticket (printed or digital) to the event", normal_style))
    story.append(Paragraph("• Arrive at least 30 minutes before the event starts", normal_style))
    story.append(Paragraph("• This ticket is non-transferable and non-refundable", normal_style))
    story.append(Paragraph("• For support, contact us at support@eventbook.com", normal_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def send_booking_confirmation_email(booking):
    """Send booking confirmation email with tickets"""
    try:
        print(f"[v0] Attempting to send confirmation email to {booking.contact_email}")
        
        # Generate PDF tickets
        pdf_buffer = generate_ticket_pdf(booking)
        
        # Prepare email content
        subject = f'🎉 Booking Confirmed - {booking.event.title} | EventVibe'
        
        context = {
            'booking': booking,
            'event': booking.event,
            'tickets': booking.tickets.all()
        }
        
        html_message = render_to_string('emails/booking_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        # Create email
        email = EmailMessage(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.contact_email],
        )
        
        email.content_subtype = 'html'
        email.body = html_message
        
        # Attach PDF
        email.attach(
            f'EventVibe_Tickets_{booking.booking_id}.pdf',
            pdf_buffer.getvalue(),
            'application/pdf'
        )
        
        # Send email
        email.send()
        
        print(f"[v0] Email sent successfully to {booking.contact_email}")
        print(f"[v0] PDF ticket attached: EventVibe_Tickets_{booking.booking_id}.pdf")
        
        return True
        
    except Exception as e:
        print(f"[v0] Error sending email: {str(e)}")
        import traceback
        print(f"[v0] Traceback: {traceback.format_exc()}")
        return False


def verify_ticket_qr(qr_data):
    """Verify ticket QR code data"""
    try:
        parts = qr_data.split('|')
        if len(parts) != 3:
            return False, "Invalid QR code format"
        
        ticket_part = parts[0].split(':')
        event_part = parts[1].split(':')
        booking_part = parts[2].split(':')
        
        if (ticket_part[0] != 'TICKET' or 
            event_part[0] != 'EVENT' or 
            booking_part[0] != 'BOOKING'):
            return False, "Invalid QR code format"
        
        ticket_id = ticket_part[1]
        event_slug = event_part[1]
        booking_id = booking_part[1]
        
        # Import here to avoid circular imports
        from .models import Ticket
        
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            
            if str(ticket.booking.booking_id) != booking_id:
                return False, "Ticket and booking ID mismatch"
            
            if ticket.booking.event.slug != event_slug:
                return False, "Ticket and event mismatch"
            
            if not ticket.is_valid:
                return False, "Ticket is not valid"
            
            return True, {
                'ticket': ticket,
                'event': ticket.booking.event,
                'booking': ticket.booking
            }
            
        except Ticket.DoesNotExist:
            return False, "Ticket not found"
        
    except Exception as e:
        return False, f"Error verifying ticket: {str(e)}"


# -------------------------------
# GPS + IP Location Validator
# -------------------------------
import requests
from geopy.distance import geodesic

ALLOWED_COUNTRY = "Nepal"

def get_ip_location(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        res = requests.get(url, timeout=3).json()
        return {
            "country": res.get("country"),
            "lat": res.get("lat"),
            "lon": res.get("lon"),
        }
    except:
        return None

def is_inside_nepal(ip_info):
    return ip_info and ip_info.get("country") == ALLOWED_COUNTRY

def gps_ip_match(user_gps, ip_info, max_distance_km=500):
    try:
        ip_point = (ip_info["lat"], ip_info["lon"])
        gps_point = (user_gps["lat"], user_gps["lon"])
        distance_km = geodesic(ip_point, gps_point).km
        return distance_km <= max_distance_km
    except:
        return False
