import os
from dotenv import load_dotenv

# Load environment variables from .env file in development
if os.path.exists(".env"):
    load_dotenv()

# Configuration class
class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    
    @staticmethod
    def validate():
        required_vars = ["GOOGLE_API_KEY", "GITHUB_TOKEN"]
        missing = [var for var in required_vars if not getattr(Config, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# Validate configuration
Config.validate() 