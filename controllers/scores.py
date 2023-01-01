def insert_score(db, score):
  match_id = score["match_id"]
  player_id = score["player_id"]
  rating = score["rating"]
  db.execute("INSERT INTO scores (match_id, player_id, rating) VALUES(%s, %s, %s)", (match_id, player_id, rating));

def get_player_avg(db, name):
    db.execute("SELECT AVG(rating) FROM scores JOIN players ON scores.player_id = players.id WHERE players.name = %s", (name,))
    return db.fetchall()

def get_last_match_score(db, name):
  db.execute("SELECT rating FROM scores JOIN players ON scores.player_id = players.id WHERE players.name = %s ORDER BY match_id DESC", (name,))
  return db.fetchall()