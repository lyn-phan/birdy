from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import server

db = SQLAlchemy()


class User(db.Model):
    """a user/handle"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    handle = db.Column(db.String(30))
    candidate_id = db.Column(
        db.Integer, db.ForeignKey('candidate.candidate_id'))

    candidate = db.relationship('Candidate', backref='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} handle={self.handle}>'


class Candidate(db.Model):
    """this keeps track of the follwers of the handle"""

    __tablename__ = 'candidate'

    candidate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    followers = db.Column(db.String(20), nullable=False)
    scrubbed_id = db.Column(db.Integer, db.ForeignKey(
        'scrubbed_candidate.scrubbed_id'))

    scrubbed_candidate = db.relationship(
        'Scrubbed_Candidate', backref='candidate')

    def __repr__(self):
        return f'<Candidate candidate_id={self.candidate_id} handle={self.handle} follower={self.filtered_follower}>'


class Scrubbed_Candidate(db.Model):
    """this is the final list after filtering the followers from candidates,
    and we're storing contact information for each candidate"""

    __tablename__ = 'scrubbed_candidate'

    scrubbed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    candidate_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=True)
    specialty = db.Column(db.String(50))

    def __repr__(self):
        return f'<Scrubbed_Candidate scrubbed_id={self.scrubbed_id} handle={self.handle}>'


def connect_to_db(app, db_uri='postgresql:///birdies', echo=True):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = echo
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    print('Connected to the database!')


if __name__ == '__main__':
    """If the model is run or imported..."""
    from server import app
    connect_to_db(app)

    db.create_all()
    # print('Connected to the database!')
