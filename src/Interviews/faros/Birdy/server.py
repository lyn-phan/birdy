"""Server file for 'a little birdy told me'"""


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
app.secret_key = os.getenv('app.secret_key')
app.jinja_env.undefined = StrictUndefined

load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

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

@app.route('/')
def homepage():
    """view homepage"""

    return render_template('home.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    """takes user input and makes a post request to get/followers_list api and returns
    matched search results"""

    handle = request.args['handle']
    quantity = request.args['quantity']
    # keyword = request.args['keyword'

    add_user = crud.add_user(handle=handle)
    print('user added')

    try:
        for follower in tweepy.Cursor(api.get_followers, screen_name=handle).items():
            # extracts followers from handle and adds to Candidate db
            followers = follower.screen_name
            added_followers = crud.add_queried_followers(followers=followers)
            print("followers worked!")

    except:
        print("Oops! That handle doesn't work. Please try again.")

    return render_template('search.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')
