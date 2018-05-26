from flask import Flask,current_app;
from flask_login import LoginManager;
from flask_migrate import Migrate  # helps in making schema changes
from flask_sqlalchemy import SQLAlchemy  # database


from app.config import Config; #Configuration class 
from flask_bootstrap import Bootstrap; #import Bootstrap
from flask_moment import Moment; #Moment is a timestamp managing libraru
import logging;

bootstrap = Bootstrap();
moment = Moment();
db = SQLAlchemy();
loginManager = LoginManager();
db_migrate = Migrate();

def create_app(config_class=Config):
    app = Flask(__name__,template_folder='templates');
    app.config.from_object(config_class);
    
    bootstrap.init_app(app);
    moment.init_app(app);
    db.init_app(app);
    db_migrate.init_app(app,db);
    loginManager.init_app(app);
    loginManager.login_view='login.login';
    
    #register error blueprint
    from app.errors import bp as errors_bp;
    app.register_blueprint(errors_bp);
    
    #register login blueprint
    from app.login import bp as login_bp;
    app.register_blueprint(login_bp);
    
    from app.home import bp as home_bp;
    app.register_blueprint(home_bp);
    
    return app;


from app import models;