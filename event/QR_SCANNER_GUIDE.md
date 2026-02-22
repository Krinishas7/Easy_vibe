# QR Scanner User Guide - EventVibe

## Complete Step-by-Step Guide to Using the QR Code Scanner

### Overview
The QR Scanner is a powerful tool for event staff to verify and admit attendees at the venue entrance by scanning the QR codes on their e-tickets.

---

## Step 1: Access the QR Scanner

### For Staff/Admin Users:

1. **Login to your account**
   - Go to the EventVibe website
   - Click "Login" in the top right corner
   - Enter your staff/admin credentials
   - Click "Sign In"

2. **Navigate to the Scanner**
   - Once logged in, click on your profile name in the top right
   - In the dropdown menu, you'll see "QR Scanner" (only visible to staff)
   - Click on "QR Scanner"
   
   **Direct URL:** `http://127.0.0.1:8000/bookings/scanner/`

---

## Step 2: Grant Camera Permissions

When you first open the scanner, your browser will ask for camera access:

### On Desktop (Chrome/Firefox/Edge):
1. A popup will appear asking "Allow camera access?"
2. Click "Allow" or "Yes"
3. If you accidentally clicked "Block", you need to:
   - Click the camera icon in the address bar
   - Select "Always allow" for camera access
   - Refresh the page

### On Mobile (iOS/Android):
1. A system prompt will appear
2. Tap "Allow" or "OK"
3. If denied, go to:
   - **iOS:** Settings > Safari > Camera > Allow
   - **Android:** Settings > Apps > Browser > Permissions > Camera > Allow

---

## Step 3: Start the Scanner

1. **Click the "Start Scanner" button**
   - The button is large and purple in the center of the screen
   - Wait 2-3 seconds for the camera to initialize

2. **Camera View Appears**
   - You'll see a live camera feed
   - A scanning frame will be visible in the center
   - The "Start Scanner" button changes to "Stop Scanner"

3. **Position the Camera**
   - Hold your device steady
   - Point the camera at the QR code on the ticket
   - Keep the QR code within the scanning frame
   - Maintain a distance of 10-30cm (4-12 inches)

---

## Step 4: Scan the QR Code

### Scanning Process:

1. **Align the QR Code**
   - Center the QR code in the camera view
   - Make sure the entire QR code is visible
   - Ensure good lighting (not too dark or too bright)

2. **Automatic Detection**
   - The scanner automatically detects and reads QR codes
   - No need to press any button
   - You'll hear a beep sound when detected (if enabled)

3. **Wait for Verification**
   - The system sends the QR data to the server
   - Verification takes 1-2 seconds
   - A result card will appear on the right side

---

## Step 5: Understanding Scan Results

### Result Types:

#### 1. **Valid Ticket (Green)**
\`\`\`
✓ Valid Ticket
Status: Confirmed
Ticket ID: TKT-ABC123
Event: Summer Music Festival
Attendee: John Doe
Email: john@example.com
Booking Date: Oct 5, 2025
\`\`\`
**Action:** Click "Admit Attendee" button to mark as used

#### 2. **Already Used (Orange)**
\`\`\`
⚠ Already Used
This ticket has already been scanned and used.
Used At: Oct 6, 2025 7:30 PM
Ticket ID: TKT-ABC123
Event: Summer Music Festival
\`\`\`
**Action:** Deny entry - ticket already admitted

#### 3. **Invalid Ticket (Red)**
\`\`\`
✗ Invalid Ticket
This ticket could not be verified.
Reason: Ticket not found or cancelled
\`\`\`
**Action:** Deny entry - ticket is not valid

#### 4. **Cancelled Booking (Red)**
\`\`\`
✗ Cancelled Booking
This booking has been cancelled.
Ticket ID: TKT-ABC123
\`\`\`
**Action:** Deny entry - booking was cancelled

---

## Step 6: Admit Attendees

### For Valid Tickets:

1. **Review the Information**
   - Check the attendee name matches their ID
   - Verify the event name is correct
   - Confirm the ticket hasn't been used

2. **Click "Admit Attendee"**
   - The button is at the bottom of the result card
   - This marks the ticket as "used"
   - The ticket cannot be used again

3. **Success Confirmation**
   - The card turns green
   - Shows "Attendee Admitted Successfully"
   - Timestamp is recorded

4. **Allow Entry**
   - Let the attendee enter the venue
   - The ticket is now marked as used in the system

---

## Step 7: View Scan History

### Scan History Panel:

Located on the right side below the current result:

\`\`\`
Scan History
─────────────
✓ TKT-ABC123 - Valid (Admitted)
  7:45 PM

✗ TKT-XYZ789 - Already Used
  7:43 PM

✓ TKT-DEF456 - Valid (Admitted)
  7:40 PM
\`\`\`

**Features:**
- Shows last 10 scans
- Color-coded by status
- Includes timestamp
- Automatically updates

---

## Step 8: Continuous Scanning

### Scanning Multiple Tickets:

1. **After Each Scan**
   - The result stays visible for review
   - You can immediately scan the next ticket
   - No need to clear or reset

2. **Scan Next Ticket**
   - Simply point camera at next QR code
   - Previous results move to history
   - New result appears at the top

3. **Rapid Scanning**
   - Scanner can process multiple tickets quickly
   - Wait for each verification to complete
   - Don't scan too fast (allow 2-3 seconds between scans)

---

## Step 9: Stop the Scanner

### When Finished:

1. **Click "Stop Scanner" button**
   - Camera feed stops
   - Camera light turns off
   - Results remain visible

2. **Review History**
   - Check scan history for any issues
   - Note any problematic tickets

3. **Close or Navigate Away**
   - You can safely close the page
   - Or navigate to other sections

---

## Troubleshooting

### Camera Not Working:

**Problem:** Camera doesn't start
**Solutions:**
- Check browser permissions (see Step 2)
- Try a different browser (Chrome recommended)
- Restart the browser
- Check if another app is using the camera

**Problem:** Camera is blurry
**Solutions:**
- Clean the camera lens
- Improve lighting conditions
- Move closer or farther from the QR code
- Hold device steady

### QR Code Not Scanning:

**Problem:** QR code not detected
**Solutions:**
- Ensure QR code is fully visible
- Improve lighting (avoid glare)
- Hold device steady
- Try different angles
- Check if QR code is damaged

**Problem:** "Invalid Ticket" error
**Solutions:**
- Verify the QR code is from EventVibe
- Check if booking was cancelled
- Confirm payment was completed
- Contact admin to verify ticket status

### Network Issues:

**Problem:** Verification takes too long
**Solutions:**
- Check internet connection
- Refresh the page
- Try again in a few seconds
- Contact IT support if persistent

---

## Best Practices

### For Efficient Scanning:

1. **Setup**
   - Test scanner before event starts
   - Ensure good lighting at entrance
   - Have backup device ready
   - Train all staff on scanner use

2. **During Event**
   - Keep device charged (use power bank)
   - Position yourself in well-lit area
   - Ask attendees to have tickets ready
   - Verify attendee ID for high-value events

3. **Communication**
   - Politely ask attendees to show ticket
   - Explain if ticket is invalid
   - Direct issues to supervisor
   - Keep line moving efficiently

4. **Security**
   - Don't share scanner access
   - Log out when finished
   - Report suspicious tickets
   - Keep device secure

---

## Quick Reference Card

### Scanner Workflow:
\`\`\`
1. Login as staff → 2. Open QR Scanner → 3. Allow camera
↓
4. Click "Start Scanner" → 5. Point at QR code → 6. Wait for result
↓
7. Review ticket info → 8. Click "Admit" if valid → 9. Allow entry
↓
10. Scan next ticket (repeat from step 5)
\`\`\`

### Status Colors:
- **Green** = Valid ticket, can admit
- **Orange** = Already used, deny entry
- **Red** = Invalid/cancelled, deny entry

### Quick Actions:
- **Valid Ticket:** Click "Admit Attendee"
- **Used Ticket:** Deny entry, explain already used
- **Invalid Ticket:** Deny entry, suggest contacting support

---

## Support

### Need Help?

**Technical Issues:**
- Contact IT Support: support@eventvibe.com
- Call: +1-234-567-8900
- Check system status: status.eventvibe.com

**Ticket Issues:**
- Verify in admin panel: /admin/bookings/ticket/
- Check booking status
- Contact event organizer

**Training:**
- Watch video tutorial: eventvibe.com/scanner-tutorial
- Practice with test tickets
- Ask supervisor for assistance

---

## Security & Privacy

### Important Notes:

1. **Access Control**
   - Only staff members can access scanner
   - Login required
   - Sessions expire after inactivity

2. **Data Privacy**
   - Ticket data is encrypted
   - Scan history is logged
   - Personal information is protected

3. **Audit Trail**
   - All scans are recorded
   - Timestamps are logged
   - Staff member is tracked

---

## Mobile vs Desktop

### Mobile Devices (Recommended):
**Pros:**
- Portable and convenient
- Built-in camera
- Easy to move around
- Better for entrance scanning

**Tips:**
- Use landscape mode for better view
- Keep screen brightness high
- Use mobile data if WiFi is weak

### Desktop/Laptop:
**Pros:**
- Larger screen
- More stable
- Better for office use

**Tips:**
- Use external webcam for better quality
- Position camera at comfortable height
- Ensure good lighting

---

## Frequently Asked Questions

**Q: Can I scan multiple tickets at once?**
A: No, scan one ticket at a time for accurate verification.

**Q: What if the QR code is on a phone screen?**
A: Yes, it works! Ask attendee to increase screen brightness.

**Q: Can I use this offline?**
A: No, internet connection required for verification.

**Q: What if I accidentally admit the wrong person?**
A: Contact admin immediately to reverse the admission.

**Q: How do I know if a ticket is fake?**
A: Invalid tickets will show "Invalid Ticket" error immediately.

**Q: Can attendees screenshot their tickets?**
A: Yes, QR codes work from screenshots, but each can only be used once.

---

## Summary

The QR Scanner is your essential tool for smooth event check-ins. Remember:

1. Always test before the event
2. Ensure good lighting and camera access
3. Verify attendee information
4. Only admit valid, unused tickets
5. Keep scan history for reference
6. Report any issues immediately

**Happy Scanning!** 🎫
