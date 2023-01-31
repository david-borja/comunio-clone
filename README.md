# FANTASY LEAGUE CLONE: SCRAPER AND FLASK APP

## INTRO

#### First some background:

Are you familiar with Fantasy League? It is an online game where users get assigned players that are part of an actual professional (soccer) league.

The better a player performs on a match, the more points the user who own it will get. Users will avoid listing injured or low performer players. Users are meant to post a lineup every week before the first game is played.

As the league advances users are allowed to sell and purchase players in order to get the most points possible every week.

By the end of the season, the user with most points wins against their mates in the group. Groups have a maximum of 16 users. 

Probably the most popular version of this game concept it the Fantasy League web app for the [Premiere League](https://fantasy.premierleague.com/).

For this Final Project, the app has been created for the Spanish soccer league, also known as [LaLiga Santander](https://www.laliga.com/laliga-santander).

#### Data issues:

Although there are some Fantasy League web apps for LaLiga (see [Biwenger](https://biwenger.as.com/)), no APIs were found in order to get player scores.

For this reason, the data had to be scraped from a website where scores are posted periodically. This website is [Comuniazo](https://www.comuniazo.com/comunio-apuestas/puntos).

## PROJECT PART 1: WEB SCRAPER AND INTEGRATOR
As said before, the project has a web scraper to get the data from Comuniazo.
This scraper can be found in /integrator.

## Technologies
  - Languages: Javascript, Python
  - Db: PostgreSQL
  - Tools: Playwright, psycopg2
  - Recommended VS Code extension: MySQL by Weijan Chen

## Get started
The project can simply be cloned: 

```
git clone git@github.com:david-borja/comunio-clone.git
```

Install dependencies both at the root folder:

```
npm i
``` 

To run the scraper go to /integrator/scores

You can scrap a single match week. To only get match week 3:
```
node index.js match=3
``` 
You can also scrap multiple weeks one after another up to a certain week.

To get all match weeks up to match week 11:
```
node index.js match=11 range=true
``` 

This will save the scores at /matches in JSON format.

In order to start inserting data in your db, first make sure you have created a PostgreSQL db named **'comuniodb' at port 5430**. Save comunio.db inside /data.

In case you want to call the db differently or create it at a different port, modify:
  - app.py line 28
  - restart_db.py line 4
  - insert_scores.py line 21
  - insert_teams.py line 12

After this, go to /integrator and run restart_db.py
```
python3 restart_db.py
``` 

This will create the tables needed for the project. 

Note: If later you need to actually **restart** your db, at restart_db.py comment the lines from 11 to 20 and run it.

Once the tables are created, start by inserting the teams.
Go to /integrator/teams and run:

```
python3 insert_teams.py
``` 

After this, scores json(s) can be integrated one by one. Important: integrate them in order. First run the script below with 1, then with 2 and so on.

Note that to integrate these json(s) they have to exist in /matches after running the scraper.

To integrate the scores of the first match week, go to /integrator/scores and run:
```
python3 insert_scores.py 1
``` 

At this point, the app is ready to be used.

## PROJECT PART 2: FLASK APP
This is a Flask application named app.py that is powered by the data gather by the scraper.


## Technologies
  - Languages: Python
  - Db: PostgreSQL
  - Tools: psycopg2
  - Recommended VS Code extension: MySQL by Weijan Chen

## Get started
To run it, simply go to the root folder and do:
```
flask run
``` 

## Functionality
  - Login/Logout
    - Form validations run on the frontend for UX and on the backend for security. Errors are handled with an apology meme.
  - Registration
    - Form validations run on the frontend for UX and on the backend for security. Errors are handled with an apology meme.
    - When registered, the user gets assigned 11 players from all the available players (not owned by other user) in the db. It randomly assigns to the user a goalkeeper, four defenders, four midfielders and two forwards.
  - Home
    - Once registered, users can check their players at the home page, sorted by position, showing each player last match score and each player average score in the season, as well as to which team players belong in real life.
    - Last match score and average score updates automatically after every match week manual integration (check Part 1)
  - Ranking
    - Users can go to Ranking to see how well are performing their players related to other users'. It shows all the users sorted by total points in the season.
    - This ranking and total points updates automatically after every match week manual integration.

## FINAL CONSIDERATIONS
This Final Project is completely independent from cs50 Codespace, implying way more environment configuration and tool research to put together different technologies.
Moreover, it was demanding to obtain the necessary data through a self-made web scraper.
For this reason, the Flask app is very rudimentary given that the overall project implied a noticeable amount of effort.

