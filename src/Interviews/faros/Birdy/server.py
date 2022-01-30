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

    handle = request.args["handle"]
    quantity = request.args["quantity"]
    keyword = request.args["keyword"]

    # adds user to the User table in database
    add_user = crud.add_user(handle)
    print("user added")

    # using the user handle, search for followers by api and adds followers to users table
    for follower in tweepy.Cursor(api.get_followers, screen_name=handle).items(2):
        try:
            followers = follower.screen_name
            # add each follower of the original handle (OH) to the database
            added_user = crud.add_user(user_handle=followers)
            # grabs id of the handle we're querying
            user_id = crud.get_userid(user_handle=followers)

        except:
            print("Oops! That handle doesn't work. Please try again.")
    # assign follow id as OH's user ID
    following_id = crud.get_userid(user_handle=handle)
    # # add each of those users(followers) as a follower to the Follower table
    added_follower = crud.add_user_as_follower(
        user_id=user_id, following_id=following_id)

    return render_template("/candidates.html", keyword=keyword, handle=handle)
    # what data needs to be returned?
    # we need the user name of our followers, along with the user ID of OH


@app.route("/candidates", methods=["GET", "POST"])
def get_relevant_candidates(keyword, handle):

    # look up user_id that corresponds with handle
    user_id = crud.get_userid(user_handle=handle)
    # look up in followers table with userID, and find following IDs
    follower_id = crud.get_follower_id(following_id=user_id)
    # go back to users table and look up corresponding screen names correspoinding with Following
    screen_name = crud.get_username(user_id=follower_id)

    print("---------------------------")
    print(screen_name)

    # run API search against all of the following_ids whose user_id = OH's ID
    # return matching screen names

    # grabs the list of followers and passes through user_Timeline API to exract tweets of corresponding users

    # for f in data():
    #     # terms = data["followers"]
    #     search_terms = keyword + "from:" + f
    #     for tweet in tweepy.Cursor(api.search_tweets, q=search_terms).items(5):
    #         if resp.ok:
    #             # collects tweet content and corresponding userID

    #             print("tweets added")
    #             return
    #         else:
    #             print("Oops, there are not matches with these followers.")

    return render_template("/candidates.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
