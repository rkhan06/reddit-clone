from flask import Blueprint

subreddit = Blueprint('subreddit', __name__)

from app.subreddit import views