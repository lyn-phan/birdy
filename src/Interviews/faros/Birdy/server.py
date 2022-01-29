"""Server file for "a little birdy told me"""


from flask import Flask, request, redirect, jsonify, render_template, flash
import sqlalchemy
from http.client import UNAUTHORIZED
from jinja2 import StrictUndefined
import os
from dotenv import load_dotenv
import tweepy
import crud
from model import *

app = Flask(__name__)
app.secret_key = os.getenv("app.secret_key")
app.jinja_env.undefined = StrictUndefined

load_dotenv()
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

### Authentication w/ Tweepy ###
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

#### Navigation ###


@app.route("/")
def homepage():
    """view homepage"""

    return render_template("home.html")


@app.route("/ingest", methods=["POST", "GET"])
def ingest():
    """takes user input and makes a post request to get/followers_list api and returns
    matched search results"""

    # if request.method == "POST":
    followers_list = []

    handle = request.form["handle"]
    quantity = request.form["quantity"]
    keyword = request.form["keyword"]

    # adds user to the database
    add_user = crud.add_user(handle)
    print("user added")
    add_keyword = crud.add_keyword(keyword)
    print("keyword added")

    # using the user handle, searches for followers by api and adds followers to the db
    try:
        for follower in tweepy.Cursor(api.get_followers, screen_name=handle, count=quantity).items():
            # extracts followers from handle and adds to Candidate db
            followers = follower.screen_name
            followers_list.append(followers)
            added_followers = crud.add_queried_followers(followers=followers)
            print("followers worked!")

    except:
        print("Oops! That handle doesn't work. Please try again.")

    return render_template("/ingest.html", followers_list=followers_list, handle=handle, keyword=keyword)


@app.route("/candidates", methods=["GET", "POST"])
def get_relevant_candidates(followers, keyword):

    followers_list = crud.get_followers(followers)
    keyword = crud.get_speciality(keyword)

    tweets = []
    # grabs the list of followers and passes through user_Timeline API to exract tweets of corresponding users
    for f in followers_list:
        search_terms = keyword + "from:" + f
        for tweet in tweepy.Cursor(api.search_tweets, q=search_terms).items(5):
            if resp.ok:
                # collects tweet content and corresponding userID
                tweets.append((tweet.text, tweet.user_id))
                print("tweets added")
            else:
                print("Oops, there are not matches with these followers.")

    return render_template("candidates.html", followers=followers, keyword=keyword)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
