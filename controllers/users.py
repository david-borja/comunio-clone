def get_user_by_name(db, username):
  db.execute("SELECT * FROM users WHERE username = %s", (username,));
  return db.fetchall()

def insert_user(db, user):
  username = user["username"]
  password = user["password"]
  db.execute("INSERT INTO users (username, hash) VALUES(%s, %s)", (username, password));