from flask import Flask
from config import Config
from flask_admin import Admin
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from mongoengine import connect

app=Flask(__name__)
app.config.from_object(Config)

# admin setting
admin = Admin(app)

# serializer token 
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# initializing the mail services 
mail = Mail(app)

urldns = "http://127.0.0.1:5001"

# database settings
try:
    # Try to connect to MongoDB using the configured connection string
    db = connect('assessment', host=app.config['MONGODB_SETTINGS']['host'])
    print("Connected to database successfully")
except Exception as e:
    print(f"Unable to connect to database: {e}")
    print("Application will run in demo mode with limited functionality")
    # For now, just use a simple dictionary to avoid database dependency
    db = None

from sapp import routes

# running the application
if __name__ == "__main__":
    app.run()
