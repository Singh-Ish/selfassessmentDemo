# ==== Configuration file ====


import os

class Config(object):

    """
    Config class defines the default configuration for the application 
    - Database
    - Flask-Admin
    - Upload Folder 
    - Email Configuration  

    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or "dev-secret-change-in-production"

    # changing the server name 
    #SERVER_NAME = '127:0.0.1:6000'

    #database setting - prioritize local MongoDB for development
    MONGODB_SETTINGS= {
        'host': os.environ.get('MONGODB_URI') or "mongodb://localhost:27017/assessment"
    }

    #admin setting
    FLASK_ADMIN_SWATCH = 'cerlean'

    #changing the server name 
    #SERVER_NAME='saportal.sce.carleton.ca'

    # file upload settings
    UPLOAD_FOLDER = 'sapp/static/docs'
    #ALLOWED_EXTENSIONS = {'pdf'}

    # Flask-Mail settings
    MAIL_SERVER = 'smtp.sce.carleton.ca'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_USERNAME =''
    MAIL_PASSWORD =''
    MAIL_DEFAULT_SENDER = ('Self-Assessment Portal',
                           'saportal@sce.carleton.ca')
