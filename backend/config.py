"""
Configuration settings for the Bank Management System.
Supports environment variables (.env) with sensible production defaults and fallback mock mode.
"""
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class AppSettings(BaseModel):
    # App General Settings
    APP_NAME: str = "Apex Bank Management System"
    APP_VERSION: str = "2.0.0"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")

    # DSA Algorithmic Engine Settings
    DEFAULT_SLIDING_WINDOW_K: int = int(os.getenv("DEFAULT_SLIDING_WINDOW_K", "3"))
    DEFAULT_FRAUD_THRESHOLD: float = float(os.getenv("DEFAULT_FRAUD_THRESHOLD", "50000.0"))

    # SMTP Mail Server Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "security@apexbank.internal")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME", "Apex National Bank")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "True").lower() in ("true", "1")
    
    # Mock SMTP Mode (automatically enabled if no credentials provided)
    MOCK_SMTP_MODE: bool = os.getenv("MOCK_SMTP_MODE", "True").lower() in ("true", "1")


settings = AppSettings()
