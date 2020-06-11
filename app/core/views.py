from flask import render_template
from app.models.user import User
from flask_login import login_required
from app.core import core


@core.route('/', methods=['GET', 'POST'])
@login_required
def index():
    users = User.query.all()
    return render_template('core/index.html', users=users)
