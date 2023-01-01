from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_ids_from_tuple(tuple):
  list = []
  for el in tuple:
    list.append(el[0])
  return list

def get_team_img_param(team_name):
    team_keys = {
        'Athletic': 1,
        'Atlético': 2,
        'Barcelona': 3,
        'Betis': 4,
        'Celta': 5,
        'Espanyol': 7,
        'Getafe': 8,
        'Mallorca': 11,
        'Osasuna': 12,
        'Real Sociedad': 13,
        'Sevilla': 17,
        'Valencia': 18,
        'Villarreal': 19,
        'Valladolid': 21,
        'Almería': 22,
        'Real Madrid': 15,
        'Rayo Vallecano': 70,
        'Elche': 75,
        'Girona': 97,
        'Cádiz': 105
    }
    return team_keys[team_name]

def get_team_name(team_id):
    team_names = [
        "Almería",
        "Athletic",
        "Atlético",
        "Barcelona",
        "Betis",
        "Cádiz",
        "Celta",
        "Elche",
        "Espanyol",
        "Getafe",
        "Girona",
        "Mallorca",
        "Osasuna",
        "Rayo Vallecano",
        "Real Madrid",
        "Real Sociedad",
        "Sevilla",
        "Valencia",
        "Valladolid",
        "Villarreal"
    ]
    return team_names[team_id - 1]