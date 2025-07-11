import os
import re
from dotenv import load_dotenv

# Monkey-patch Markup for flaskext.markdown
from markupsafe import Markup as _Markup
import flask
flask.Markup = _Markup

from flask import Flask, url_for, Markup
from flask_cors import CORS
from flaskext.markdown import Markdown
from markdown import Markdown as PyMarkdown

from .extensions import db, migrate  # Your SQLAlchemy + Migrate instances

# Load environment variables
load_dotenv()

# Regex to match Obsidian-style images ![[filename.ext]]
OBSIDIAN_IMAGE_RE = re.compile(r"!\[\[([^\]]+?)\]\]")

# Initialize standalone Python-Markdown parser with desired extensions
md_parser = PyMarkdown(extensions=[
    'fenced_code',
    'codehilite',
    'tables',
    'toc',
    'extra'
])

def render_md_obsidian(content, post_id):
    """
    Replace Obsidian-style image links with standard Markdown and render HTML.
    """
    def replace(match):
        filename = match.group(1)
        # Build URL to /static/images/<post_id>/filename
        img_url = url_for('static', filename=f'images/{post_id}/{filename}')
        return f'![]({img_url})'

    # Substitute all ![[...]] patterns
    prepped = OBSIDIAN_IMAGE_RE.sub(replace, content)
    # Convert to HTML
    html = md_parser.reset().convert(prepped)

    # 3a) Anchors *without* any class → inject the attribute
    html = re.sub(
        r'<a(?=[^>]*\bhref="https?://)(?![^>]*\bclass=)',
        '<a class="external-link"',
        html,
        flags=re.IGNORECASE
    )

    # 3b) Anchors *with* an existing class → append to it
    html = re.sub(
        r'class="([^"]+)"(?=[^>]*\bhref="https?://)',
        r'class="\1 external-link"',
        html,
        flags=re.IGNORECASE
    )
    
    return Markup(html)


def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(
        __name__,
        static_folder='static',
        static_url_path='/static',
        template_folder=os.path.join(base_dir, 'templates')
    )
    CORS(app)

    # Register the Obsidian-wiki image filter
    app.jinja_env.filters['md_obsidian'] = render_md_obsidian

    # Optionally keep basic Markdown filter
    Markdown(app, extensions=['extra', 'toc'])

    # --- Application Config ---
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Upload folder points to /path/to/app/static
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static')

    # Initialize database + migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
