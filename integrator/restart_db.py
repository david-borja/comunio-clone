import psycopg2

# Open a DB session
dbSession = psycopg2.connect("dbname='comuniodb' port='5430'");

# Open a database cursor
dbCursor = dbSession.cursor();

# dbCursor.execute("DROP TABLE teams CASCADE");
dbCursor.execute("DROP TABLE users CASCADE");
dbCursor.execute("DROP TABLE players CASCADE");
dbCursor.execute("DROP TABLE matches CASCADE");
dbCursor.execute("DROP TABLE scores CASCADE");

# dbCursor.execute("""CREATE TABLE teams (
#     id SERIAL PRIMARY KEY, 
#     name TEXT NOT NULL
#   )"""
# );

dbCursor.execute("""CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  hash TEXT NOT NULL,
  points NUMERIC NOT NULL DEFAULT 0
)""");

dbCursor.execute("""CREATE TABLE players (
    id SERIAL PRIMARY KEY, 
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    position_id INTEGER,
    team_id INTEGER,
    user_id INTEGER DEFAULT NULL,
    listed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(team_id) REFERENCES teams(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
  )"""
);

dbCursor.execute("""CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    week INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    FOREIGN KEY(home_team_id) REFERENCES teams(id),
    FOREIGN KEY(away_team_id) REFERENCES teams(id)
  )"""
);

dbCursor.execute("""CREATE TABLE scores (
    id SERIAL PRIMARY KEY,
    rating NUMERIC NOT NULL,
    player_id INTEGER,
    match_id INTEGER,
    FOREIGN KEY(player_id) REFERENCES players(id),
    FOREIGN KEY(match_id) REFERENCES matches(id)
  )"""
);


dbSession.commit()
# Close the session and free up the resources   
dbSession.close();  