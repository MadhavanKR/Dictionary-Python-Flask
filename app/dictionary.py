from app import create_app,db;
from app.models import User,Words;
import os,logging;
from logging.handlers import SMTPHandler,RotatingFileHandler;
import logging;

app = create_app();

#code for logging to a file
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs');
    file_handler = RotatingFileHandler('logs/dcitionary.log', maxBytes=10240, backupCount=10);
    file_handler.setLevel(logging.INFO);
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'));
    app.logger.addHandler(file_handler);
    app.logger.setLevel(logging.INFO);
    app.logger.info('MicroBlog startup');


@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User,'Words':Words};
