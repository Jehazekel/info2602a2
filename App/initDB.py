from main import db, app #, Pokemon, MyPokemon
import csv

db.create_all(app=app)

# add code to parse csv, create and save pokemon objects

# replace any null values with None to avoid db errors
