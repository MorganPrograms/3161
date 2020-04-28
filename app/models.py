from . import db
from werkzeug.security import generate_password_hash


class UserProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(80))
    Last_name = db.Column(db.String(80))
    Username = db.Column(db.String(80), unique=True)
    Password = db.Column(db.String(255))
    Gender = db.Column(db.String(6))
    Email = db.Column(db.String(80))
    Location = db.Column(db.String(80))
    Biography = db.Column(db.String(255))
    File = db.Column(db.String(50))
    date_joined = db.Column(db.String(50))

    def __init__(self,fname,lname,username,password,gender,email,location,bio,file,joined):
        self.First_name = fname
        self.Last_name = lname
        self.Username = username
        self.Password = generate_password_hash(password, method='pbkdf2:sha256')
        self.Gender = gender
        self.Email = email
        self.Location = location
        self.Biography = bio
        self.File = file
        self.date_joined = joined

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
