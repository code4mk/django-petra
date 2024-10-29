from dotenv import load_dotenv
import os

def load_env():
    """Load environment variables from .env file."""
    load_dotenv()

def get_env(key: str, default=None) -> str:
    """
    Retrieve environment variable value.
    
    Args:
        key: The environment variable key
        default: Default value if key is not found
        
    Returns:
        The environment variable value or default if not found
    """
    return os.getenv(key, default)