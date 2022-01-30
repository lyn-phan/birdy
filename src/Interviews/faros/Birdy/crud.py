""" CRUD Operation """

from flask import Flask, session
from model import *


def add_user(user_handle):
    """create and returns any user """

    user = User(user_handle=user_handle)
    db.session.add(user)
    db.session.commit()

    return user


def add_user_as_follower(user_id, following_id):
    """ adds original handle and it's followers"""

    user_followers = Follower(user_id=user_id, following_id=following_id)
    db.session.add(user_followers)
    db.session.commit()

    return user_followers


def get_follower_id(userid):
    """look up following ID (who's following a given user) by giving it a user id"""
    first_id = Follower.query.filter_by(following_id=userid).first()
    follower_id = first_id.following_id

    return follower_id


def get_username(user_id):
    """looks up screen name by user ID"""

    sn = User.query.filter_by(user_id=user_id).first()
    name = sn.user_handle

    return name


def get_userid(user_handle):
    """looks up userID by handle"""

    userid = User.query.filter_by(user_handle=user_handle).first()
    user_id = userid.user_id

    return user_id


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
