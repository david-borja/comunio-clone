
# ----- Example Python program to insert data into a PostgreSQL database table
import psycopg2
import json

with open('teams.json') as teams_file:
  teams = teams_file.read()

teams_json = json.loads(teams)
# Open a DB session

dbSession = psycopg2.connect("dbname='comuniodb' port='5430'");

# Open a database cursor

dbCursor = dbSession.cursor();

# Insert statements

for team in teams_json:
  print(team)
  dbCursor.execute("INSERT INTO teams (name) VALUES (%s)", [team]);

# It is essential to commit the transaction else it will be rollbacked 

dbSession.commit();

# Close the session and free up the resources   
dbSession.close();  