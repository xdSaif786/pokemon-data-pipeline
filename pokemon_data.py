import requests
import pandas as pd
import sqlite3
pokemon = ('https://pokeapi.co/api/v2/pokemon')
param = {"limit" : 151}
response = requests.get(pokemon, params=param)
print(f"Status code: {response.status_code}")
data = (response.json())
detailed_pokemon =[]
pokemon_list = data["results"]
for i in pokemon_list:
    pokemon_details = requests.get(i["url"])
    detailed_response = (pokemon_details.json())
    poke_details = {
        "id" : detailed_response["id"] ,
        "name" : detailed_response["name"],
        "height" : detailed_response["height"],
        "weight" : detailed_response["weight"],
        "base_experience" : detailed_response["base_experience"]
    }
    detailed_pokemon.append(poke_details)
print(detailed_pokemon)

df = pd.DataFrame(detailed_pokemon)
df['BMI'] = (df['weight'] / 10) / ((df['height'] / 10) ** 2)
median_weight = df['weight'].median()
df['weightclass'] = df['weight'].apply(lambda w: 'heavyweight' if w >= median_weight else 'lightweight')

conn = sqlite3.connect("detailed_pokemon.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS pokemon (
id INTEGER PRIMARY KEY,
name TEXT,
height INTEGER,
weight INTEGER,
base_experience INTEGER,
BMI REAL,
weightclass TEXT
);
""")
conn.commit()
c.execute("DELETE FROM pokemon")
df.to_sql("pokemon", conn, if_exists = "append", index = False)
conn.commit()
conn.close()

print (df)

