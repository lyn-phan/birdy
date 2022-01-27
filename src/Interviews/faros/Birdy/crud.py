""" CRUD Operation """

from flask import Flask, session
from model import *


def add_user(handle):
    """create and returns handle that we're searching with"""

    user = User(handle=handle)
    db.session.add(user)
    db.session.commit()

    return user


def add_queried_followers(followers):
    """ adds original handle and it's followers based on filters"""

    user_followers = Candidate(followers=followers)
    db.session.add(user_followers)
    db.session.commit()

    print("followers added!")


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
