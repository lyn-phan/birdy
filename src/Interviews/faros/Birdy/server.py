"""Server file for "a little birdy told me"""


from flask import Flask, request, redirect, render_template, session
import sqlalchemy
from http.client import UNAUTHORIZED
from jinja2 import StrictUndefined
import os
from dotenv import load_dotenv
import tweepy
import crud
from model import *
import json

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


@app.route("/ingest/")
def ingest():
    """takes user input and makes a post request to get/followers_list api and returns
    matched search results"""

    followers_list = []

    user_handle = request.args["handle"]
    quantity = request.args["quantity"]
    keyword = request.args["keyword"]
    keyword = str(keyword)

    # adds user to the User table in database
    add_user = crud.add_user(user_handle=user_handle)
    # <User user_id=7 handle=marvin_roque>

    # using the user handle, search for followers by api and adds followers to users table
    for follower in tweepy.Cursor(api.get_followers, screen_name=user_handle).items(10):
        try:
            followers = str(follower.screen_name)
            followers_list.append(followers)
            # add each follower of the original handle (OH) to the database
            added_user = crud.add_user(user_handle=followers)
            # grabs id of the followers' handles
            user_id = crud.get_userid(user_handle=followers)

        except:
            print("Oops! That handle doesn't work. Please try again.")
    # assign follow id as OH's user ID
    following_id = crud.get_userid(user_handle=user_handle)
    # # add each of those users(followers) as a follower to the Follower table
    added_follower = crud.add_user_as_follower(
        user_id=user_id, following_id=following_id)

    # # get list of followers names
    # make an API call to search_tweets. loop through list of followers and pass in search
    # terms from keyword user input and return list of users corresponding with that search query
    for follow in followers_list:

        search_terms = f"\'{keyword} from:{follow}\'"
        try:
            searched_tweets = [tweet for tweet in tweepy.Cursor(
                api.search_tweets, q=search_terms).items(50)]

            for t in searched_tweets:
                found_sn = t.user.screen_name

        except:
            print("Oops, there are not matches with these followers.")

    return render_template("/candidates.html", keyword=keyword, user_handle=user_handle, found_sn=found_sn)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
