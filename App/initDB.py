from main import db, app #, Pokemon, MyPokemon
import csv

global data

db.create_all(app=app)

# add code to parse csv, create and save pokemon objects
with open("App/pokemon.csv") as f:
    data= json.load(f)

for pokemon in data:
    record= Pokemon(
        pid= pokemon['pid'],
        name= pokemon['name'], 
        attack= pokemon['attack'],
        defense= pokemon['defense'],
        hp= pokemon['hp'],
        height= pokemon['height']
        sp_attack= pokemon['sp_attack']
        sp_defense= pokemon['sp_defense'],
        speed= pokemon['speed'],
        weight= pokemon['weight']
        type1= pokemon['type1'],
        if pokemon['type2'] != ""
            type2= pokemon['type2']
        else
            type2="none"
            

    )
    db.session.add(record)

db.session.commit()

# replace any null values with None to avoid db errors
