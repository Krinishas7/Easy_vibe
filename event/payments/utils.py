import hashlib
import hmac
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def generate_esewa_signature(message, secret_key):
    """Generate HMAC signature for eSewa"""
    return hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def verify_esewa_payment(product_id, amount, reference_id):
    """Verify payment with eSewa"""
    try:
        # eSewa verification URL (test environment)
        verification_url = "https://rc.esewa.com.np/epay/transrec"
        
        
        verification_data = {
            'amt': amount,
            'rid': reference_id,
            'pid': product_id,
            'scd': settings.ESEWA_MERCHANT_ID
        }
        
        response = requests.post(verification_url, data=verification_data, timeout=30)
        
        if response.status_code == 200:
            response_text = response.text.strip()
            
            # eSewa returns "Success" for successful verification
            if "Success" in response_text:
                return {
                    'status': 'success',
                    'message': 'Payment verified successfully',
                    'response': response_text
                }
            else:
                return {
                    'status': 'failed',
                    'message': 'Payment verification failed',
                    'response': response_text
                }
        else:
            return {
                'status': 'error',
                'message': f'Verification request failed with status {response.status_code}'
            }
            
    except requests.exceptions.Timeout:
        logger.error('eSewa verification timeout')
        return {
            'status': 'error',
            'message': 'Verification request timed out'
        }
    except Exception as e:
        logger.error(f'eSewa verification error: {str(e)}')
        return {
            'status': 'error',
            'message': 'Verification request failed'
        }


def format_esewa_amount(amount):
    """Format amount for eSewa (should be string with 2 decimal places)"""
    return f"{float(amount):.2f}"


def validate_esewa_response(request_data):
    """Validate eSewa response data"""
    required_fields = ['oid', 'amt', 'refId']
    
    for field in required_fields:
        if not request_data.get(field):
            return False, f'Missing required field: {field}'
    
    # Additional validation can be added here
    try:
        float(request_data['amt'])
    except ValueError:
        return False, 'Invalid amount format'
    
    return True, 'Valid'
