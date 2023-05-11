from flask import Flask
from .routes import auth_bp
app = Flask(__name__)


app.register_blueprint(auth_bp, strict_slashes=False)
