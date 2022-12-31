import psycopg2
import json
import sys

sys.path.append('../../controllers') 
from matches import insert_match, get_match_id
from players import insert_player, get_player_id
from scores import insert_score

week = sys.argv[1]
file_path = './matches/scoresMatch{}.json'.format(week)
with open(file_path) as scores_file:
  scores = scores_file.read()
scores_json = json.loads(scores)

with open('../teams/teams.json') as teams_file:
  teams = teams_file.read()
teams_json = json.loads(teams)

# Open a DB session
dbSession = psycopg2.connect("dbname='comuniodb' port='5430'");

# Open a database cursor
dbCursor = dbSession.cursor();

for match in scores_json:
  teams = match.split(' - ')
  home_team = teams[0]
  away_team = teams[1]
  home_team_index = teams_json.index(home_team) + 1
  away_team_index = teams_json.index(away_team) + 1

  match_obj = {
    "week": week,
    "home_team_index": home_team_index,
    "away_team_index": away_team_index
  }
  insert_match(dbCursor, match_obj)
  print("Inserted MATCH with week {}, home_team_index {}, away_team_index {}".format(week, home_team_index, away_team_index))
  match_id = get_match_id(dbCursor, match_obj).fetchone()[0]
  
  match_teams = scores_json[match]
  for team in match_teams:
      players = match_teams[team]
      for player in players:
        score = players[player]['score']
        position = players[player]['position']
        team_id = home_team_index if team == 'homePlayers' else away_team_index
        player_obj = {
          "name": player,
          "team_id": team_id
        }
        rows_num = get_player_id(dbCursor, player_obj).rowcount
        if rows_num == 0:
          player_obj["position"] = position
          insert_player(dbCursor, player_obj)
          del player_obj["position"]
        player_id = get_player_id(dbCursor, player_obj).fetchone()[0]
        score_obj = {
          "match_id": match_id,
          "player_id": player_id,
          "rating": score
        }
        insert_score(dbCursor, score_obj)
        print("Inserted SCORE with match_id {}, player_id {}, score {}".format(match_id, player_id, score))

# It is essential to commit the transaction else it will be rollbacked 
dbSession.commit();

# Close the session and free up the resources   
dbSession.close();  