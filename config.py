import os
from dotenv import load_dotenv
import torch

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 1024 * 1024 * 1024))  # Default 1GB
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
