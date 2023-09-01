from dotenv import load_dotenv

def setup_environment(location: str) -> None:
    """Load environment variables from a file if specified, else from .env (defaults)"""
    if location:
        load_dotenv(location)
    else:
        load_dotenv()
