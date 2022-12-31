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

def update_player_user_id(db, player_id, user_id):
  db.execute("UPDATE players SET user_id = %s WHERE id = %s", (user_id, player_id))

def get_free_players(db, position, limit):
    db.execute("SELECT * FROM players WHERE user_id IS NULL AND position = %s ORDER BY random() LIMIT %s", (position, limit))
    return db.fetchall()
