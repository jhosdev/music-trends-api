#__init__.py
from flask import Flask
import os
from src.auth import auth
from src.artists import artists

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECREY_KEY"),

        )

    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route('/')
    def index():
        return 'Music Trends API'
    
    app.register_blueprint(auth)
    app.register_blueprint(artists)

    return app