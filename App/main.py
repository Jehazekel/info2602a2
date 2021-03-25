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


@app.route('/mypokemon', methods=["POST"])
@jwt_required()
def save_mypokemon():
    data= request.get_json()    #get the user name and pokemon id 
    user= User.query.filter_by(username=data['name']).first()
    if user!= None:
        user= user.toDict()
        pokemon= Pokemon.query.get(data['pid'])
        mypokemon= MyPokemon(pid=data['pid'], id=user['id'], name= user['username'],pokemon= pokemon)
        db.session.add(mypokemon)
        db.session.commit()
        return data['name'] + " captured"
    return "No Pokemon captured!"


@app.route('/mypokemon', methods=["GET"])
@jwt_required()
def list_mypokemon():
    username = current_identity.username
    user= User.query.filter_by(username= username).first()
    if user:
        user_id= user.id
        user_pokemons= MyPokemon.query.filter_by(id= user_id)
        user_pokemons= [pokemon.toDict() for pokemon in user_pokemons]
        return json.dumps( user_pokemons )
    return "No Pokemon captured!"


@app.route('/mypokemon/<user_nth_pokemon>', methods=["GET"])
@jwt_required()
def get_mypokemon(user_nth_pokemon):
    username= current_identity.username
    user= User.query.filter_by(username= username).first()
    if user:
        user_id= user.id
        all_user_pokemons= MyPokemon.query.filter_by(id= user_id)
        all_user_pokemons= [pokemon.toDict() for pokemon in all_user_pokemons]
        if int(user_nth_pokemon) <= len(all_user_pokemons): 
            nth_pokemon= all_user_pokemons[int(user_nth_pokemon) - 1]
            return json.dumps(nth_pokemon)
    return "No Pokemon captured!"


#Allows a user to rename their pokemon
@app.route('/mypokemon/<user_nth_pokemon>', methods=["PUT"])
@jwt_required()
def update_mypokemon(user_nth_pokemon):
    data= request.get_json()
    username= current_identity.username
    user= User.query.filter_by(username= username).first()
    if user:
        user_id= user.id
        all_user_pokemons= MyPokemon.query.filter_by(id= user_id)
        all_user_pokemons= [pokemon for pokemon in all_user_pokemons]
        if int(user_nth_pokemon) <= len(all_user_pokemons): 
            nth_pokemon= all_user_pokemons[int(user_nth_pokemon) - 1]
            nth_pokemon.pokemon.name= data['name']
            db.session.add(nth_pokemon)
            db.session.commit()
            return "Updated"
        return "No Pokemon found!"
    return "Invalid User!"


#Allows a user to release their pokemon
@app.route('/mypokemon/<user_nth_pokemon>', methods=["DELETE"])
@jwt_required()
def delete_mypokemon(user_nth_pokemon):
    username= current_identity.username
    user= User.query.filter_by(username= username).first()
    if user:
        user_id= user.id
        all_user_pokemons= MyPokemon.query.filter_by(id= user_id)
        all_user_pokemons= [pokemon for pokemon in all_user_pokemons]
        if int(user_nth_pokemon) <= len(all_user_pokemons): 
            nth_pokemon= all_user_pokemons[int(user_nth_pokemon) - 1]
            db.session.delete(nth_pokemon)
            db.session.commit()
            return "Deleted", 204
        return "No Pokemon found!"
    return "Invalid User!"



@app.route('/app')
def client_app():
  return app.send_static_file('app.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)