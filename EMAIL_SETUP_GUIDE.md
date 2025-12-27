# Email Configuration Guide for EventVibe

This guide will help you set up email functionality so that booking confirmations with e-tickets are automatically sent to customers.

## Current Status

The email system is **already implemented** and will work automatically once configured. When a customer completes a booking and payment:

1. ✅ A confirmation email is sent to the customer's email address
2. ✅ The email includes a PDF attachment with all tickets
3. ✅ Each ticket has a unique QR code for entry verification
4. ✅ The email is beautifully formatted with event details

## Development Mode (Current Setup)

In development mode (DEBUG=True), emails are printed to the **console/terminal** instead of being sent. This is perfect for testing without needing real email credentials.

**To see emails in development:**
1. Run your Django server: `python manage.py runserver`
2. Complete a booking and payment
3. Check your terminal - you'll see the full email content printed there

## Production Mode (Real Email Sending)

To send real emails to customers, follow these steps:

### Option 1: Gmail (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate an App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "EventVibe" or "Django App"
   - Copy the 16-character password

3. **Update your `.env` file:**
   \`\`\`env
   DEBUG=False
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_16_character_app_password
   DEFAULT_FROM_EMAIL=EventVibe <your_email@gmail.com>
   \`\`\`

4. **Restart your Django server**

### Option 2: Other Email Providers

#### Outlook/Hotmail
\`\`\`env
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@outlook.com
EMAIL_HOST_PASSWORD=your_password
\`\`\`

#### Yahoo Mail
\`\`\`env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@yahoo.com
EMAIL_HOST_PASSWORD=your_app_password
\`\`\`

#### Custom SMTP Server
\`\`\`env
EMAIL_HOST=your_smtp_server.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_username
EMAIL_HOST_PASSWORD=your_password
\`\`\`

## Testing Email Functionality

### Test 1: Check Console Output (Development)
\`\`\`bash
# Make sure DEBUG=True in .env
python manage.py runserver

# Complete a booking through the website
# Check terminal for email output
\`\`\`

### Test 2: Send Test Email (Production)
\`\`\`bash
# Run the test email script
python scripts/send_test_email.py
\`\`\`

### Test 3: Complete Real Booking
1. Set up email credentials (see above)
2. Set `DEBUG=False` in `.env`
3. Restart server
4. Complete a booking with a real email address
5. Check the email inbox

## Troubleshooting

### Emails not appearing in console
- **Check:** Is `DEBUG=True` in your `.env` file?
- **Check:** Is the server running when you complete the booking?
- **Solution:** Look for `[v0]` prefixed messages in the terminal

### Gmail "Less secure app" error
- **Problem:** Gmail blocks login attempts from apps
- **Solution:** Use App Passwords (see Gmail setup above)
- **Never:** Lower your account security settings

### Emails not being sent (Production)
- **Check:** Is `DEBUG=False`?
- **Check:** Are email credentials correct in `.env`?
- **Check:** Is your email provider allowing SMTP access?
- **Check:** Look for error messages in terminal with `[v0]` prefix

### PDF attachment missing
- **Check:** Are tickets being generated? (Check booking detail page)
- **Check:** Is the `media` folder writable?
- **Solution:** Run `python manage.py collectstatic`

### Email sent but not received
- **Check:** Spam/Junk folder
- **Check:** Email address is correct in booking form
- **Check:** Email provider's sending limits (Gmail: 500/day)

## Email Flow Diagram

\`\`\`
Customer Books Ticket
        ↓
Payment Successful
        ↓
Booking Status → "Confirmed"
        ↓
Generate Tickets with QR Codes
        ↓
Generate PDF with All Tickets
        ↓
Send Email with PDF Attachment
        ↓
Customer Receives Email
\`\`\`

## What's Included in the Email

✅ **Beautiful HTML Email** with EventVibe branding
✅ **Event Details** (date, time, venue, address)
✅ **Booking Summary** (booking ID, quantity, amount)
✅ **Individual Ticket Information** for each ticket
✅ **PDF Attachment** with all tickets and QR codes
✅ **Important Instructions** for event entry

## Security Notes

- Never commit your `.env` file to version control
- Use App Passwords, not your main email password
- Keep `EMAIL_HOST_PASSWORD` secret
- In production, use environment variables instead of `.env` file
- Consider using a dedicated email service (SendGrid, Mailgun) for high volume

## Production Recommendations

For a production event booking system, consider:

1. **Dedicated Email Service**
   - SendGrid (12,000 free emails/month)
   - Mailgun (5,000 free emails/month)
   - Amazon SES (62,000 free emails/month)

2. **Email Queue**
   - Use Celery for asynchronous email sending
   - Prevents slow page loads during email sending

3. **Email Monitoring**
   - Track delivery rates
   - Monitor bounce rates
   - Handle unsubscribe requests

## Support

If you encounter issues:
1. Check the terminal for `[v0]` debug messages
2. Verify your email credentials
3. Test with a simple email first
4. Check your email provider's documentation

---

**Note:** The email system is fully functional and ready to use. Just configure your email credentials and it will work automatically!
