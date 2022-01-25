from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.sql import func

db = SQLAlchemy()


class User(db.Model):
    """a user/handle"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    original_handle = db.Column(
        db.String(30), nullable=False)

    candidate = db.relationship('Candidate', backref='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} handle={self.original_handle}>'


class Candidate(db.Model):
    """this keeps track of the follwers of the original_handle"""

    __tablename__ = 'candidate'

    candidate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    original_handle = db.Column(
        db.String(30), db.ForeignKey('user.original_handle'), nullable=False)
    filtered_follower = db.Column(db.String(20), nullable=False)

    user = db.relationship('user', backref='candidate')

    def __repr__(self):
        return f'<Candidate candidate_id={self.candidate_id} handle={self.original_handle} follower={self.filtered_follower}>'


class Scrubbed_Candidate(db.Model):
    """this is the final list after filtering the followers from candidates,
    and we're storing contact information for each candidate"""

    __tablename__ = 'scrubbed_candidate'

    scrubbed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    original_handle = db.Column(db.String(30), db.ForeignKey(
        'user.original_handle'), nullable=False)
    original_handle = db.Column(db.String(30), db.ForeignKey(
        'candidate.original_handle'), nullable=False)
    candidate_name = db.Column(db.String(40))
    handle = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=True)

    user = db.relationship('user', backref='scrubbed_candidate')
    candidate = db.relationship('candidate', backref='scrubbed_candidate')

    def __repr__(self):
        return f'<Scrubbed_Candidate scrubbed_id={self.scrubbed_id} original_handle={self.original_handle}>'


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///birdies'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    """If the model is run or imported..."""
    from server import app
    connect_to_db(app)

    db.create_all()
    print('Connected to the database!')
