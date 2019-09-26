from redis import Redis
import rq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models


def create_app(config_class=Config):
	app.redis = Redis.from_url(app.config['REDIS_URL'])
	app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)