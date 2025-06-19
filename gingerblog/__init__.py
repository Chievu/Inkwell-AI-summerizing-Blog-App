import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv
from markupsafe import Markup, escape
from flask_caching import Cache 

# Load the env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'sensitive.env'))

from gingerblog.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
csrf = CSRFProtect()

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})  

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    cache.init_app(app)

    # Ensure all models are imported so Alembic can detect them properly
    from gingerblog.models import User, Post, Like

    # Register Blueprints
    from gingerblog.main.routes import main
    from gingerblog.users.routes import users
    from gingerblog.posts.routes import posts
    from gingerblog.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    def nl2br(value):
        escaped = escape(value)
        return Markup(escaped.replace('\n', '<br>\n'))
    app.jinja_env.filters['nl2br'] = nl2br

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Post': Post, 'Like': Like}

    return app
