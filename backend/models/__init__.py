# backend/__init__.py (CORRECTED CORS Initialization)

from flask import Flask
from .user import User
from backend.config import Config
from backend.extensions import db, migrate, cors
from .lead import Lead
from .otp import OTP

def create_app(config_class=Config):
    # ... (app setup)

    # Initialize Extensions
    # ... (db, migrate init)

    # VVV --- DEFINITIVE CORS FIX --- VVV
    cors.init_app(create_app, resources={r"/api/*": {
        "origins": [
            "http://localhost:3000",       # Localhost is the standard React address
            "http://127.0.0.1:3000",       # 127.0.0.1 is the local IP address
            "*"                            # Fallback wildcard
        ],
        "supports_credentials": True, # Recommended for complex requests
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"] # Ensure all methods are allowed
    }})
    # ^^^ --------------------------- ^^^
    
    # ... (rest of the file)