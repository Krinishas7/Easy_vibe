# Event Booking System

A comprehensive Django-based event booking system that allows users to browse events, book tickets, and make payments through eSewa gateway. Administrators can manage events, track bookings, and monitor sales through a powerful admin dashboard.

## Features

### User Features
- **User Registration & Authentication**: Secure user accounts with profile management
- **Event Browsing**: Search and filter events by category, date, and location
- **Ticket Booking**: Easy booking process with real-time availability checking
- **Payment Integration**: Secure payments through eSewa gateway
- **E-Tickets**: Downloadable PDF tickets with QR codes for verification
- **Booking Management**: View and manage personal bookings
- **Email Notifications**: Automatic booking confirmations via email

### Admin Features
- **Event Management**: Create, update, and manage events with categories
- **Booking Oversight**: Monitor all bookings with detailed analytics
- **Payment Tracking**: Track payment status and transaction details
- **User Management**: Manage user accounts and profiles
- **Sales Analytics**: Revenue tracking and ticket sales reports
- **Bulk Operations**: Efficient bulk actions for managing large datasets

### Technical Features
- **QR Code Generation**: Unique QR codes for each ticket for entry verification
- **PDF Generation**: Professional ticket PDFs with event details
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Email System**: Automated email notifications and confirmations
- **Payment Verification**: Secure payment verification with eSewa API
- **Data Validation**: Comprehensive form validation and error handling

## Technology Stack

- **Backend**: Django 4.2.7, Python 3.8+
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Payment**: eSewa Payment Gateway
- **PDF Generation**: ReportLab
- **QR Codes**: qrcode library
- **Email**: Django Email Framework

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd event-booking-system
   \`\`\`

2. **Create virtual environment**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Environment Configuration**
   \`\`\`bash
   cp .env.example .env
   # Edit .env file with your configuration
   \`\`\`

5. **Database Setup**
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   python scripts/create_database.py  # Creates sample data and admin user
   \`\`\`

6. **Run the development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

7. **Access the application**
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/
   - Default admin credentials: admin/admin123

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

\`\`\`env
SECRET_KEY=your-secret-key-here
DEBUG=True
ESEWA_MERCHANT_ID=your-esewa-merchant-id
ESEWA_SECRET_KEY=your-esewa-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@eventbook.com
\`\`\`

### eSewa Configuration

1. Register for an eSewa merchant account
2. Get your merchant ID and secret key
3. Update the environment variables
4. Configure success/failure URLs in settings

### Email Configuration

For production, configure SMTP settings:
- Gmail: Use app-specific passwords
- Other providers: Update EMAIL_HOST and EMAIL_PORT in settings

## Usage

### For Users

1. **Registration**: Create an account with email verification
2. **Browse Events**: Search and filter available events
3. **Book Tickets**: Select quantity and provide contact details
4. **Payment**: Complete payment through eSewa gateway
5. **Download Tickets**: Get PDF tickets with QR codes
6. **Manage Bookings**: View booking history and status

### For Administrators

1. **Access Admin Panel**: Login with admin credentials
2. **Manage Events**: Create and update event information
3. **Monitor Bookings**: Track all bookings and payments
4. **Generate Reports**: View sales analytics and revenue data
5. **User Management**: Manage user accounts and permissions

## Management Commands

### Create Sample Events
\`\`\`bash
python manage.py create_sample_events --count 20
\`\`\`

### Cleanup Expired Bookings
\`\`\`bash
python manage.py cleanup_expired_bookings --hours 24
\`\`\`

### Verify Tickets
\`\`\`bash
python manage.py verify_ticket <ticket_number>
\`\`\`

## Testing

Run the test suite:
\`\`\`bash
python manage.py test
\`\`\`

Run specific app tests:
\`\`\`bash
python manage.py test events
python manage.py test bookings
\`\`\`

## API Endpoints

### Public Endpoints
- `GET /` - Home page with featured events
- `GET /events/` - Event listing with search/filter
- `GET /events/<id>/` - Event details
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login

### Authenticated Endpoints
- `GET /bookings/` - User's bookings
- `POST /bookings/create/` - Create new booking
- `GET /bookings/<id>/` - Booking details
- `GET /accounts/profile/` - User profile

### Payment Endpoints
- `POST /payments/initiate/` - Initiate eSewa payment
- `GET /payments/success/` - Payment success callback
- `GET /payments/failure/` - Payment failure callback

## Deployment

### Production Checklist

1. **Security Settings**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use strong `SECRET_KEY`
   - Enable HTTPS

2. **Database**
   - Use PostgreSQL for production
   - Configure database backups
   - Set up connection pooling

3. **Static Files**
   - Configure static file serving
   - Use CDN for media files
   - Enable compression

4. **Email**
   - Configure production SMTP
   - Set up email templates
   - Enable email logging

5. **Monitoring**
   - Set up error logging
   - Configure performance monitoring
   - Enable health checks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: support@eventbook.com
- Documentation: [Project Wiki]
- Issues: [GitHub Issues]

## Changelog

### Version 1.0.0
- Initial release with core booking functionality
- eSewa payment integration
- QR code ticket generation
- Admin dashboard
- Email notifications
