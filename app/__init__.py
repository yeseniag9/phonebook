from flask import Flask #, render_template **
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder

app = Flask(__name__) # This is the line that actually runs our app
CORS(app) # CORS is a security thing; it will help prevent cross-site request forgery (common way hackers access our data)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app) # Initiate the app; make the database
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)