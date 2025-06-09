from flask import Flask
from .config import Config
from .extensions import mongo, bcrypt, jwt
from .routes import auth, habits, logs

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(habits)
    app.register_blueprint(logs)
    
    return app
