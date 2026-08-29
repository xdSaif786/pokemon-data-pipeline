import sqlite3
conn = sqlite3.connect("detailed_pokemon.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS pokemon (
id INTEGER PRIMARY KEY,
name TEXT,
height INTEGER,
weight INTEGER,
base_experience INTEGER,
body_mass REAL,
weightclass TEXT
);
""")
conn.commit()

c.execute("""
SELECT weightclass, AVG(base_experience), MAX(body_mass)
FROM pokemon
GROUP BY weightclass;
""")
rows = c.fetchall()
for row in rows:
    print(row)