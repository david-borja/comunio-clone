def get_user_by_name(db, username):
  db.execute("SELECT * FROM users WHERE username = %s", (username,));
  return db.fetchall()

def insert_user(db, user):
  username = user["username"]
  password = user["password"]
  db.execute("INSERT INTO users (username, hash) VALUES(%s, %s)", (username, password));

def get_all_user_ids(db):
    db.execute("SELECT id FROM users");
    return db.fetchall()

def compute_user_points(db, user_id):
  db.execute("SELECT SUM(rating) FROM scores JOIN players ON scores.player_id = players.id WHERE user_id = %s", (user_id,));
  return db.fetchall()

def update_user_points(db, user_id, points):
    db.execute("UPDATE users SET points = %s WHERE id = %s", (points, user_id))

def get_ranked_users(db):
  db.execute("SELECT id, username, points FROM users ORDER BY points DESC")
  return db.fetchall()

