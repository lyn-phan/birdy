from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import server

db = SQLAlchemy()


class User(db.Model):
    """a user/handle"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_handle = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} handle={self.user_handle}>'


class Follower(db.Model):
    """this keeps track of the followers of the original handle"""

    __tablename__ = "follower"

    f_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), nullable=False)

    user = db.relationship("User", backref="follower",
                           foreign_keys=[user_id])
    follows = db.relationship(
        "User", foreign_keys=[following_id])

    def __repr__(self):
        return f'<Follower f_id={self.f_id} user_id={self.user_id} following_id={self.following_id}>'


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
