from flask import Flask
from config import Config
from mongoengine import connect
from flask_admin import Admin
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer





app=Flask(__name__)

# running the application
if __name__ == "__main__":
    app.run()
    
app.config.from_object(Config)

# admin setting
admin = Admin(app)


# serializer token 
s = URLSafeTimedSerializer('SECRET_KEY')

# initializing the mail services 
mail = Mail(app)

urldns = "http://127.0.0.1:5000"
# adding the API for the application
#api=Api()
#api.init_app(app)





# database settings
try:
    # Connect to a local MongoDB instance instead of cloud for now
    db = connect('assessment', host='localhost', port=27017)
    print("Connected to local database successfully")
except Exception as e:
    print(f"Unable to connect to database: {e}")
    # For now, just use a simple dictionary to avoid database dependency
    db = None



from sapp import routes
