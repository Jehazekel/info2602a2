import json
from flask import Flask, request, render_template
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 


from models import db, Pokemon, MyPokemon, User
''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) 
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()


''' End Boilerplate Code '''

''' Set up JWT here '''

def authenticate(uname, password):
  #search for the specified user
  user = User.query.filter_by(username=uname).first()
  #if user is found and password matches
  if user and user.check_password(password):
    return user

#Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)

''' End JWT Setup '''

# edit to query 50 pokemon objects and send to template
@app.route('/', methods=['GET'])
def index():
    pokemons= Pokemon.query.offset(0).limit(50).all()
    return render_template('listing.html', pokemons= pokemons)


@ app.route('/pokemon', methods=['GET'])
def pokemon_listing():
    pokemons= Pokemon.query.all()
    pokemons= [pokemon.toDict() for pokemon in pokemons]            
    return json.dumps(pokemons) 

@app.route('/signup',methods=['POST'])
def signup():
    userdata = request.get_json() # get json data (aka submitted username, email & password)
    newuser = User(username=userdata['username'], email=userdata['email']) # create user object
    newuser.set_password(userdata['password']) # set password
    try:
        db.session.add(newuser)
        db.session.commit() # save user
    except IntegrityError: # attempted to insert a duplicate user
        db.session.rollback()
        return 'username or email already exists' # error message
    return 'user created' # success




@app.route('/app')
def client_app():
  return app.send_static_file('app.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)