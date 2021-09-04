from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets Module (Given by Python)
import secrets

# Imports for Login Manager and Flask Login
from flask_login import UserMixin, LoginManager

# Imports for Flask Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
lm = LoginManager()
ma = Marshmallow()

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    hero = db.relationship('Hero', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id='', password='', token='', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database.'

# MUST INCLUDE THE FOLLWING
# - id (Integer)
# - name (String)
# - description (String)
# - comics_appeared_in (Integer)
# - super_power (String)
# - date_created (DateTime w/ datetime.utcnow)
# - owner (FK to User using the user's token)

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hero_name = db.Column(db.String(150))
    real_name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,hero_name,real_name,description,comics_appeared_in,super_power,user_token,id=0):
        self.id = self.set_id()
        self.hero_name = hero_name
        self.real_name = real_name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.user_token = user_token

    def __repr__(self):
        return f'The following hero card has been added: {self.hero_name}'

    def set_id(self):
        return (secrets.token_urlsafe())

# Creation of api schema via the marshmallow object
class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id','hero_name','real_name','description','comics_appeared_in','super_power']

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)
