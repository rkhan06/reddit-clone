from flask import render_template
from app.models.user import User
from app.models.subreddit import Subreddit
# from flask_login import login_required
from app.core import core


@core.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    subreddits = Subreddit.query.all()
    return render_template('core/index.html', users=users,
                           subreddits=subreddits)
