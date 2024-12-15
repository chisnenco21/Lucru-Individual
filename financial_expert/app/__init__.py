from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .config import Config

csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    csrf.init_app(app)
    
    from .routes import bp
    app.register_blueprint(bp)
    
    return app