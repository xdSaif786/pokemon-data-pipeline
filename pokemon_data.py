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
df['body_mass'] = df['weight'] / (df['height'] ** 2)
median_weight = df['weight'].median()
df['weightclass'] = df['weight'].apply(lambda w: 'heavyweight' if w >= median_weight else 'lightweight')

df.to_sql("pokemon", sqlite3.connect("detailed_pokemon.db"), if_exists = "replace", index = False)


print (df)

