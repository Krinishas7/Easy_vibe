#!/usr/bin/env python
"""
Test script to verify email configuration is working correctly.
This script will attempt to send a test email to verify your SMTP settings.
"""

import os
import sys
import django

# ---------------------------
# Setup Django environment
# ---------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils.html import strip_tags

# ---------------------------
# Recipient Email
# ---------------------------
RECIPIENT_EMAIL = 'ashimbashyal13@gmail.com'  # <-- change if needed

# ---------------------------
# Test Functions
# ---------------------------

def test_simple_email():
    """Test sending a simple text email"""
    print("\n" + "="*60)
    print("TEST 1: Simple Text Email")
    print("="*60)
    
    try:
        send_mail(
            subject='Test Email from EventVibe',
            message='This is a test email to verify your email configuration is working correctly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[RECIPIENT_EMAIL],
            fail_silently=False,
        )
        print("✅ Simple email sent successfully!")
        print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"   To: {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Failed to send simple email: {str(e)}")
        return False


def test_html_email():
    """Test sending an HTML email"""
    print("\n" + "="*60)
    print("TEST 2: HTML Email")
    print("="*60)
    
    try:
        html_content = """
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white; padding: 30px; border-radius: 10px; text-align: center;">
                    <h1>🎉 EventVibe Email Test</h1>
                    <p>Your email configuration is working perfectly!</p>
                </div>
                <div style="padding: 20px;">
                    <h2>Email Settings Verified:</h2>
                    <ul>
                        <li>✅ SMTP Connection Successful</li>
                        <li>✅ HTML Rendering Working</li>
                        <li>✅ Email Delivery Functional</li>
                    </ul>
                    <p>You're all set to send booking confirmations!</p>
                </div>
            </body>
        </html>
        """
        
        plain_content = strip_tags(html_content)
        
        email = EmailMessage(
            subject='EventVibe HTML Email Test',
            body=plain_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[RECIPIENT_EMAIL],
        )
        email.content_subtype = 'html'
        email.body = html_content
        email.send()
        
        print("✅ HTML email sent successfully!")
        print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"   To: {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Failed to send HTML email: {str(e)}")
        return False


def test_email_with_attachment():
    """Test sending an email with attachment"""
    print("\n" + "="*60)
    print("TEST 3: Email with Attachment")
    print("="*60)
    
    try:
        email = EmailMessage(
            subject='EventVibe Email with Attachment Test',
            body='This email includes a test attachment to verify PDF ticket delivery works.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[RECIPIENT_EMAIL],
        )
        
        # Create a simple text file as attachment
        attachment_content = "This is a test attachment from EventVibe.\nYour ticket PDFs will be attached like this."
        email.attach('test_ticket.txt', attachment_content, 'text/plain')
        
        email.send()
        
        print("✅ Email with attachment sent successfully!")
        print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"   To: {RECIPIENT_EMAIL}")
        print(f"   Attachment: test_ticket.txt")
        return True
    except Exception as e:
        print(f"❌ Failed to send email with attachment: {str(e)}")
        return False


# ---------------------------
# Display Current Settings
# ---------------------------
def display_current_settings():
    print("\n" + "="*60)
    print("CURRENT EMAIL CONFIGURATION")
    print("="*60)
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Default From Email: {settings.DEFAULT_FROM_EMAIL}")
    
    if settings.DEBUG:
        print("\n⚠️  DEBUG MODE: Emails will be printed to console")
        print("   To send real emails, set DEBUG=False in .env")
    else:
        print(f"\nSMTP Host: {getattr(settings, 'EMAIL_HOST', 'Not configured')}")
        print(f"SMTP Port: {getattr(settings, 'EMAIL_PORT', 'Not configured')}")
        print(f"Use TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not configured')}")
        print(f"Host User: {getattr(settings, 'EMAIL_HOST_USER', 'Not configured')}")
        print(f"Password: {'*' * 16 if getattr(settings, 'EMAIL_HOST_PASSWORD', '') else 'Not configured'}")


# ---------------------------
# Main Function
# ---------------------------
def main():
    print("\n" + "="*60)
    print("EVENTVIBE EMAIL CONFIGURATION TEST")
    print("="*60)
    print("\nThis script will test your email configuration.")
    
    display_current_settings()
    
    print("\n" + "="*60)
    print("RUNNING EMAIL TESTS")
    print("="*60)
    
    results = []
    results.append(("Simple Text Email", test_simple_email()))
    results.append(("HTML Email", test_html_email()))
    results.append(("Email with Attachment", test_email_with_attachment()))
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Your email configuration is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Please check your email configuration in .env file.")
    print("="*60 + "\n")
    
    if settings.DEBUG:
        print("💡 TIP: Check your terminal/console for the email content (DEBUG mode).")
    else:
        print("💡 TIP: Check your email inbox (and spam folder).")


# ---------------------------
# Run Script
# ---------------------------
if __name__ == '__main__':
    main()
