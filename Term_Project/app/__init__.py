from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config


db = SQLAlchemy()
#bootstrap = Bootstrap()

login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()



def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER

    db.init_app(app)
    #Functions bellow will break program
    #Add login with init_app() then uncommit for it to not break

    login.init_app(app)
    moment.init_app(app)
    Bootstrap(app)
    #bootstrap.init_app(app)

    from app.Controller.errors import bp_errors as errors
    app.register_blueprint(errors)

    from app.Controller.auth_routes import bp_auth as auth
    app.register_blueprint(auth)

    from app.Controller.routes import bp_routes as routes
    app.register_blueprint(routes)

    

    return app