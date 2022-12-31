def insert_player(db, player):
  name = player["name"]
  team_id = player["team_id"]
  position = player["position"]

  db.execute("INSERT INTO players (name, team_id, position) VALUES(%s, %s, %s)", (name, team_id, position));

def get_player_id(db, player):
  name = player["name"]
  team_id = player["team_id"]
  db.execute("SELECT id FROM players WHERE name = %s AND team_id = %s", (name, team_id));
  return db;