from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from .routes import main
    app.register_blueprint(main)
    CORS(app)
    return app