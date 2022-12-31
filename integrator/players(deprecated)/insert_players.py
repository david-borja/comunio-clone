import psycopg2
import json

with open('players.json') as players_file:
  players = players_file.read()
players_json = json.loads(players)

with open('../teams/teams.json') as teams_file:
  teams = teams_file.read()
teams_json = json.loads(teams)

# Open a DB session
dbSession = psycopg2.connect("dbname='comuniodb' port='5430'");

# Open a database cursor
dbCursor = dbSession.cursor();

# Insert statements

for player in players_json:
  player_obj = players_json[player]
  position = player_obj["position"]
  team = player_obj["team"]
  team_index = teams_json.index(team) + 1
  dbCursor.execute("INSERT INTO players (name, position, team_id) VALUES(%s, %s, %s)", (player, position, team_index));

# It is essential to commit the transaction else it will be rollbacked 
dbSession.commit();

# Close the session and free up the resources   
dbSession.close();  