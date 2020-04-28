from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# Config Values
USERNAME = 'admin'
PASSWORD = 'password123'
UPLOAD_FOLDER = './app/static/uploads'

# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
SECRET_KEY = 'Sup3r$3cretkey'

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dbproject:1@localhost/dbproject"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
