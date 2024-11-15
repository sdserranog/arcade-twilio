import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class TwilioConfig:
    """Twilio configuration settings."""
    account_sid: str
    api_key_sid: str
    api_key_secret: str
    from_phone_number: str
    my_phone_number: str

def load_config(env_file: str = "arcade.env") -> TwilioConfig:
    """
    Load Twilio configuration from environment variables.
    
    Args:
        env_file: Path to the environment file (default: "arcade.env")
        
    Returns:
        TwilioConfig object containing all necessary credentials
        
    Raises:
        ValueError: If any required environment variables are missing
    """
    load_dotenv(env_file)
    
    required_vars = [
        "TWILIO_ACCOUNT_SID",
        "TWILIO_API_KEY_SID",
        "TWILIO_API_KEY_SECRET",
        "TWILIO_PHONE_NUMBER",
        "MY_PHONE_NUMBER"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return TwilioConfig(
        account_sid=os.environ["TWILIO_ACCOUNT_SID"],
        api_key_sid=os.environ["TWILIO_API_KEY_SID"],
        api_key_secret=os.environ["TWILIO_API_KEY_SECRET"],
        from_phone_number=os.environ["TWILIO_PHONE_NUMBER"],
        my_phone_number=os.environ["MY_PHONE_NUMBER"]
    )