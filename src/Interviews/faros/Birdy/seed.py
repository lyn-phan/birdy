from model import *
import os
import crud
import server

os.system('dropdb birdies')
os.system('createdb birdies')

connect_to_db(server.app)
db.create_all()


def get_users(db):
    return db.session.execute("""
        SELECT user_id, user_handle 
        FROM user """).fetchall()


def seed_database(db):
    user1 = User(user_handle='_lyndalove')
    user2 = User(user_handle='marbeeno')
    follower1 = Follower(user_id=1, following=2)
    follower2 = Follower(user_id=2, following=1)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(follower1)
    db.session.add(follower2)
    db.session.commit()


seed_database(db)
