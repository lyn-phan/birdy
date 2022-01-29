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


def get_followers(followers):
    potential_candidates = Candidate.query.filter_by(followers=followers).all()

    return list(potential_candidates)


def add_keyword(keyword):
    saved_keyword = Candidate(keyword=keyword)
    db.session.add(saved_keyword)
    db.session.commit()

    print("keyword added!")
    return saved_keyword


def get_speciality(keyword):
    keyword = Candidate.query.filter_by(keyword=keyword).all()

    return keyword


    # def s = ():
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
