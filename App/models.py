from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class MyPokemon(db.Model):
  bid = db.Column('bid', db.Integer, primary_key=True)
  id = db.Column('id', db.Integer, db.ForeignKey('user.id'))
  pid = db.Column('pid', db.Integer, db.ForeignKey('pokemon.pid'))
  name = db.Column(db.String(50))
  pokemon = db.relationship('Pokemon')
  

  def toDict(self):
    return{
      'name':self.name,
      'stats':self.pokemon.toDict()
    }

## Create a User Model
class User(db.Model):
    id = db.Column('id',db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False )
    email= db.Column('email',db.String(80), unique= True, nullable= False)
    password= db.Column('password', db.String(80), nullable= False)
## must have set_password, check_password and to Dict
    def toDict(self):
        return{
            'id': self.id,
            'username':self.username,
            'email':self.email,
            'password': self.password
        }

    def set_password(self, password):
        self.password= generate_password_hash(password, method='sha256')

    def check_password(self, password ):
        return check_password_hash(self.password,password )

    
## Create a Pokemon Model
class Pokemon(db.Model):
    pid = db.Column('pid', db.Integer, primary_key=True)
    name= db.Column(db.String(50))
    attack= db.Column(db.Integer)
    defense= db.Column(db.Integer)
    hp= db.Column(db.Float)
    height= db.Column(db.Integer, nullable=True)
    sp_attack = db.Column(db.Integer)
    sp_defense = db.Column(db.Integer)
    speed= db.Column(db.Integer)
    type1= db.Column(db.String(50))
    type2= db.Column(db.String(50), nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    
    def toDict(self):
        return{
            'pid':self.pid,
            'name':self.name,
            'attack':self.attack,
            'defense':self.defense,
            'hp':self.hp,
            'height':self.height,
            'sp_attack':self.sp_attack,
            'sp_defense':self.sp_defense,
            'speed':self.speed,
            'type1':self.type1,
            'type2':self.type2,
            'weight':self.weight
        }
