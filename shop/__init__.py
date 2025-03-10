from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename  # Ensure this import is correct

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

import os
#from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_whooshee import Whooshee

basedir = os.path.abspath(os.path.dirname(__file__))

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myshop.db"
app.config['SECRET_KEY']='hfouewhfoiwefoquw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize the app with the extension
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
#photos = UploadSet('photos', IMAGES)
#configure_uploads(app, photos)
#patch_request_class(app)

db = SQLAlchemy(app)
search = Whooshee()
search.init_app(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login first"

from shop.products import routes
from shop.admin import routes