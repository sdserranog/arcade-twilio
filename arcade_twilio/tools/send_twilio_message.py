from twilio.rest import Client
from loguru import logger
from .config import TwilioConfig

def send_twilio_message(config: TwilioConfig, to_number: str, message: str, is_whatsapp: bool = False) -> str:
    """
    Send a message using Twilio.
    
    Args:
        config: TwilioConfig instance
        to_number: Destination phone number
        message: Message content
        is_whatsapp: Whether to send as WhatsApp message
        
    Returns:
        Message SID
    """
    client = Client(config.api_key_sid, config.api_key_secret, config.account_sid)
    
    # Resolve phone number
    number = config.my_phone_number if to_number == "my_phone_number" else to_number
    
    # Format numbers for WhatsApp if needed
    if is_whatsapp:
        from_number = f"whatsapp:{config.from_phone_number}"
        to_number = f"whatsapp:{number}"
    else:
        from_number = config.from_phone_number
        to_number = number
        
    response = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )
    logger.info(f"Message sent successfully, SID: {response.sid}")
    return response.sid