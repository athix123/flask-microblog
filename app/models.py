from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import redis
import rq


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	# Redis Queue
	# tasks = db.relationship('Task', backref='user', lazy='dynamic')
	#

	def __repr__self(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# class Task(db.Model):
# 	id = db.Column(db.String(36), primary_key=True)
# 	name = db.Column(db.String(128), index=True)
# 	description = db.Column(db.String(128))
# 	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
# 	complete = db.Column(db.Boolean, default=False)

# 	def get_rq_job(self):
# 		try:
# 			rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
# 		except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
# 			return None
# 		return rq_job


# 	def get_progress(self):
# 		job = self.get_rq_job()
# 		return job.meta.get('progress', 0) if job is not None else 100