import os

# Monkey-patch: make sure Markup is available for Flask-Markdown
from markupsafe import Markup
import flask
flask.Markup = Markup

from flask import Flask
from dotenv import load_dotenv
from .extensions import db, migrate  # Import both db and migrate
from flask_cors import CORS
from flaskext.markdown import Markdown

load_dotenv()

def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    simple_flask = Flask(__name__, static_folder='static', static_url_path='/static', template_folder=os.path.join(base_dir, 'templates'))
    CORS(simple_flask)
    Markdown(simple_flask, extensions=['extra', 'toc'])  # Enable Markdown support

    simple_flask.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    simple_flask.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    simple_flask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    simple_flask.config['UPLOAD_FOLDER'] = os.path.join(simple_flask.root_path, 'static')

    db.init_app(simple_flask)
    migrate.init_app(simple_flask, db)  # Initialize Flask-Migrate

    from .routes import main
    simple_flask.register_blueprint(main)

    return simple_flask
