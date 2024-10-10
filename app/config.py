# Importing necessary libraries

import os
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()

# Creating a class to get the API key from environment variables

class Settings:
    api_key = os.getenv("API_KEY")
    data_name = os.getenv("BOT_DATA")
    
    # List of allowed origins (origins that can make cross-origin requests)
    origins = [
        "https://cbot.losyro.com",
        "http://localhost:8000",
        "127.0.0.1:57830",
        "http://localhost:57830",
        "http://localhost:3000",
        "127.0.0.1:3000"
    ]
    # Add more origins if needed

settings = Settings()
