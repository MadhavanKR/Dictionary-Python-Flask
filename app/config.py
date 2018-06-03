import os

basedir = '/Users/m0k00eu/python-projects/dictionary/app/';

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess';
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +basedir+'app.db';
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    WORDS_PER_PAGE=3;
    
    QUIZ_NUM_QUESTIONS = 10;
    
    #Mail server configurations
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['madhavan.kalkunte@gmail.com']
    
    #password_reset
    SECRET_KEY = 'i am batman';
    
    #translations
    LANGUAGES = ['en', 'es'];
    
    #elasticseach
    ELASTIC_URL= os.environ.get('ELASTIC_URL');
