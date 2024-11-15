from typing import Annotated
from arcade.sdk import tool
from .config import load_config
from .send_twilio_message import send_twilio_message


@tool
def send_whatsapp(
    phone_number: Annotated[
        str,
        "The phone number to send the message to. Use 'my_phone_number' when a phone number is not specified or when the request implies sending to the user themselves",
    ],
    message: Annotated[str, "The text content to be sent via WhatsApp"],
) -> str:
    """Send a WhatsApp message to a phone number"""
    config = load_config()
    sid = send_twilio_message(config, phone_number, message, is_whatsapp=True)
    return f"Message sent successfully, SID: {sid}"
