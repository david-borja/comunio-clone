def insert_match(db, match):
  week = match["week"]
  home_team_index = match["home_team_index"]
  away_team_index = match["away_team_index"]
  db.execute("INSERT INTO matches (week, home_team_id, away_team_id) VALUES(%s, %s, %s)", (week, home_team_index, away_team_index));

def get_match_id(db, match):
  week = match["week"]
  home_team_index = match["home_team_index"]
  away_team_index = match["away_team_index"]
  db.execute("SELECT id FROM matches WHERE week = %s AND home_team_id = %s AND away_team_id = %s", (week, home_team_index, away_team_index));
  return db;