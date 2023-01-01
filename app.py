import psycopg2
import sys
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology, get_ids_from_tuple, get_team_img_param, get_team_name

sys.path.append('./controllers') 
from matches import insert_match, get_match_id
from players import insert_player, get_player_id, update_player_user_id, get_free_players, get_user_players
from scores import insert_score, get_player_avg, get_last_match_score
from users import get_user_by_name, insert_user, update_user_points, compute_user_points, get_all_user_ids, get_ranked_users

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Open a DB session
dbSession = psycopg2.connect("dbname='comuniodb' port='5430'");

# Open a database cursor
dbCursor = dbSession.cursor();

# Generate password hash
method = "pbkdf2:sha256"
salt_len = 8

@app.after_request
# after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    if user_id:
      rows = get_user_players(dbCursor, user_id)
      players = []
      last_match_total = 0
      for row in rows:
        name = row[1]
        team = get_team_name(row[4])
        team_path = get_team_img_param(team)
        team_file_path = "{}.png".format(str(team_path))
        position = row[2]
        rows = get_player_avg(dbCursor, name)
        avg = rows[0][0]
        last_score = get_last_match_score(dbCursor, name)[0][0]
        last_match_total += last_score
        player = {
          'name': name,
          'team': team,
          'team_pic': team_file_path,
          'position': position,
          'avg': "{:.1f}".format(avg),
          'last_score': last_score
        }
        players.append(player)
        print(last_match_total)
      return render_template("index.html", players=players, last_match_total=last_match_total)
    else:
      return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database username
        rows = get_user_by_name(dbCursor, request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
      return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
      username = request.form.get("username")
      password = request.form.get("password")
      confirmation = request.form.get("confirmation")

      regis_info = {
          "username": username,
          "password": password,
          "confirmation": confirmation
      }

      for field in regis_info:
          field_value = regis_info[field]
          if not field_value:
              return apology('must provide {}'.format(field))

          rows = get_user_by_name(dbCursor, username)
          if len(rows):
            return apology('user already exists')
          
          # Passwords do not match
          if password != confirmation:
            return apology("passwords do not match")
          
          user_obj = {
            "username": username,
            "password": generate_password_hash(password, method, salt_len)
          }
          insert_user(dbCursor, user_obj)
          dbSession.commit()
          user = get_user_by_name(dbCursor, username)

          user_id = user[0][0]

          # Remember which user has logged in
          session["user_id"] = user_id

          # Assign players
          free_goalkeepers = get_free_players(dbCursor, 'Goalkeeper', 1)
          free_midfielders = get_free_players(dbCursor, 'Midfielder', 4)
          free_defenders = get_free_players(dbCursor, 'Defender', 4)
          free_forwards = get_free_players(dbCursor, 'Forward', 2)
          free_player_ids = get_ids_from_tuple(free_goalkeepers) + get_ids_from_tuple(free_midfielders) + get_ids_from_tuple(free_defenders) + get_ids_from_tuple(free_forwards)

          for player_id in free_player_ids:
            update_player_user_id(dbCursor, player_id, user_id)
            dbSession.commit()
          return redirect("/")
  else:
    return render_template("register.html")
  
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/ranking")
@login_required
def ranking():
  rows = get_all_user_ids(dbCursor)
  for row in rows:
    user_id = row[0]
    points = compute_user_points(dbCursor, user_id)[0][0]
    update_user_points(dbCursor, user_id, points)
    dbSession.commit()
  rows = get_ranked_users(dbCursor)
  ranked_users = []
  rank_pos = 0
  for row in rows:
    name = row[1]
    points = "{:.1f}".format(row[2])
    rank = rank_pos + 1
    rank_pos += 1

    user = {
      "name": name,
      "points": points,
      "rank": rank
    }
    ranked_users.append(user)
  return render_template("ranking.html", ranked_users=ranked_users)
