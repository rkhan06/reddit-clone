from flask import render_template, request, redirect, url_for, jsonify
from flask_login import current_user

from app import db
from app.models.subreddit import Subreddit
from app.models.post import Post
from app.models.comment import Comment
from flask_login import login_required
from app.core import core
from app.core.forms import PostForm, ImageForm, LinkForm
from app.subreddit.forms import EmptyForm


@core.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    subreddits = Subreddit.query.all()
    empty_form = EmptyForm()
    return render_template('core/index.html',
                           subreddits=subreddits, posts=posts,
                           empty_form=empty_form)


@core.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    postform = PostForm(prefix='postform')
    imageform = ImageForm(prefix='imageform')
    linkform = LinkForm(prefix='linkform')
    default_choice = [(0, 'Choose Community')]
    linkform.community.choices = imageform.community.choices = \
        postform.community.choices = default_choice + [
            (sub.id, "r/"+sub.name) for sub in Subreddit.query.all()]

    if request.method == 'POST':
        # submit post form
        if postform.validate_on_submit() and postform.submit.data:
            community = Subreddit.query.filter_by(
                id=postform.community.data).first()
            new_post = Post(title=postform.title.data.strip(),
                            description=postform.description.data.strip(),
                            subreddit=community,
                            author=current_user)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('core.index'))
        # submit link post
        if linkform.validate_on_submit() and linkform.submit.data:
            community = Subreddit.query.filter_by(
                id=linkform.community.data).first()
            new_post = Post(title=linkform.title.data,
                            link=linkform.link.data,
                            subreddit=community,
                            author=current_user)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('core.index'))

    return render_template('core/create_post.html', postform=postform,
                           imageform=imageform, linkform=linkform)


@core.route('/upvote', methods=['POST'])
def upvote():
    if not current_user.is_authenticated:
        response = {
            'status':  'Not Authorized',
            'message': 'Please login or signup to vote',
            'link': url_for('auth.login')
        }
        return jsonify(response), 200

    data = request.get_json()
    post = Post.query.filter_by(id=data['post_id']).first()
    response = dict()
    if post is not None:
        res = post.upvote(current_user)
        db.session.commit()
        response['message'] = 'success'
        response['value'] = res
        response['votes'] = post.votes()
        return jsonify(response), 200

    response['message'] = 'error'

    return jsonify(response), 200


@core.route('/downvote', methods=['POST'])
def downvote():
    if not current_user.is_authenticated:
        response = {
            'status':  'Not Authorized',
            'message': 'Please login or signup to vote',
            'link': url_for('auth.login')
        }
        return jsonify(response), 200
    data = request.get_json()
    post = Post.query.filter_by(id=data['post_id']).first()
    response = dict()
    if post is not None:
        res = post.downvote(current_user)
        db.session.commit()
        response['message'] = 'success'
        response['value'] = res
        response['votes'] = post.votes()
        return jsonify(response), 200

    response['message'] = 'error'

    return jsonify(response), 200


@core.route('/comment_upvote', methods=['POST'])
def comment_upvote():
    if not current_user.is_authenticated:
        response = {
            'status':  'Not Authorized',
            'message': 'Please login or signup to vote',
            'link': url_for('auth.login')
        }
        return jsonify(response), 200

    data = request.get_json()
    comment = Comment.query.filter_by(id=data['comment_id']).first()
    response = dict()
    if comment is not None:
        res = comment.upvote(current_user)
        db.session.commit()
        response = {
            'status': "success",
            'message': 'upvoted comment successfully',
            'value': res,
            'votes': comment.votes()
        }
        return jsonify(response), 200

    response = {
        'status':  'error',
        'message': 'Comment does not exist'
    }

    return jsonify(response), 200


@core.route('/comment_downvote', methods=['POST'])
def comment_downvote():
    if not current_user.is_authenticated:
        response = {
            'status':  'Not Authorized',
            'message': 'Please login or signup to vote',
            'link': url_for('auth.login')
        }
        return jsonify(response), 200

    data = request.get_json()
    comment = Comment.query.filter_by(id=data['comment_id']).first()
    response = dict()
    if comment is not None:
        res = comment.downvote(current_user)
        db.session.commit()
        response = {
            'status': "success",
            'message': 'downvoted comment successfully',
            'value': res,
            'votes': comment.votes()
        }
        return jsonify(response), 200

    response = {
        'status':  'error',
        'message': 'Comment does not exist'
    }

    return jsonify(response), 200
