def get_user_by_name(db, username):
  db.execute("SELECT id FROM users WHERE username = %s", (username,));
  return db.fetchall()