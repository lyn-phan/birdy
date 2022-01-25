from model import User, Candidate, Scrubbed_Candidate, connect_to_db, db
import os
import crud
import server

os.system('dropdb birdies')
os.system('createdb birdies')

connect_to_db(server.app)
db.create_all()


def get_users(db):
    return db.session.execute("""
        SELECT user_id, original_handle 
        FROM user """).fetchall()


def seed_database(db):
    user = User(original_handle='_lyndalove')
    candidate = Candidate(original_handle='_lyndalove',
                          filtered_follower='Ebitie')
    scrubbed_candidate = Scrubbed_Candidate(original_handle='_lyndalove',
                                            candidate_name='Ebitie',
                                            handle='Ebitie')

    db.session.add(user)
    db.session.add(candidate)
    db.session.add(scrubbed_candidate)
    db.session.commit()

    return user


seed_database(db)
