def insert_score(db, score):
  match_id = score["match_id"]
  player_id = score["player_id"]
  rating = score["rating"]
  db.execute("INSERT INTO scores (match_id, player_id, rating) VALUES(%s, %s, %s)", (match_id, player_id, rating));