from flask import Flask
from .config import Config
from .extensions import mongo, bcrypt, jwt
from .routes import auth, habits, logs

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(habits)
    app.register_blueprint(logs)
    
    return app
