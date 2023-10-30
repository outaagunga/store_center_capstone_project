import os
from dotenv import load_dotenv


# Loading the .env file
load_dotenv()


class Config:
    # Database configurations
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI");
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
    
    # Mail Configurations
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))  # Default to 587 if not provided
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)  # Default to True if not provided
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT =os.environ.get('SECURITY_PASSWORD_SALT')