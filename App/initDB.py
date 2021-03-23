from main import db, app
from models import Pokemon, MyPokemon, User
import csv

global data

db.create_all(app=app)

# add code to parse csv, create and save pokemon objects
with open("App/pokemon.csv", "r") as csv_file:
    data = csv.DictReader(csv_file)
    

    
    for pokemon in data:
        
        print(pokemon, "\n\n")   

        if pokemon['type2'] != '':
            sec_type= pokemon['type2']
        else:
            sec_type="none"
    
        record= Pokemon(
            pid= pokemon['pokedex_number'],
            name= pokemon['name'], 
            attack= pokemon['attack'],
            defense= pokemon['defense'],
            hp= pokemon['hp'],
            height= pokemon['height_m'],
            sp_attack= pokemon['sp_attack'],
            sp_defense= pokemon['sp_defense'],
            speed= pokemon['speed'],
            weight= pokemon['weight_kg'],
            type1= pokemon['type1'],
            type2= sec_type
  
        )
        db.session.add(record)
        

    
    db.session.commit() 
# replace any null values with None to avoid db errors
