import sqlite3
conn = sqlite3.connect("detailed_pokemon.db")
c = conn.cursor()
try:
    c.execute("""
SELECT weightclass, AVG(base_experience), MAX(BMI)
FROM pokemon
GROUP BY weightclass;
""")
    rows = c.fetchall()
    for row in rows:
        print(row)
    c.execute("SELECT COUNT(*) FROM pokemon")
    print(c.fetchone())
except sqlite3.OperationalError:
    print("No data yet: please run pokemon_data.py first")
conn.close()