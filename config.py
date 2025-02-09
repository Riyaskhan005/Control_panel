import os

class Config:
    # Set the secret key to secure sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')

    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance
    SQLALCHEMY_ECHO = False  # Set to True for SQL query logs (optional for debugging)

    # Set the MySQL database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:Riyas123@localhost/customer')
