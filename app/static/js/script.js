$(document).ready(function () {
    replaceClass = function (oldClass, newClass, id) {
        var elem = document.getElementById(id);
        elem.classList.remove(oldClass);
        elem.classList.add(newClass);
    }


    upvote = function (post_id) {
        data = {
            post_id: post_id
        }
        fetch('/upvote', {
            method: 'post',
            body: JSON.stringify(data),
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            upvoteId = 'upvote-' + post_id;
            downvoteId = 'downvote-' + post_id;
            if (data.value === 1) {
                replaceClass('icon', 'icon-voted', upvoteId)
                replaceClass('icon-voted', 'icon', downvoteId)
                document.getElementById('votes-' + post_id).innerHTML = data.votes;
            }
            if (data.status === 'Not Authorized') {
                window.location.href = data.link;
            }
            else {
                replaceClass('icon-voted', 'icon', upvoteId)
                document.getElementById('votes-' + post_id).innerHTML = data.votes;
            }
        });
    }

    downvote = function (post_id) {
        data = {
            post_id: post_id
        }
        fetch('/downvote', {
            method: 'post',
            body: JSON.stringify(data),
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            downvoteId = 'downvote-' + post_id;
            upvoteId = 'upvote-' + post_id;
            if (data.value === 1) {
                replaceClass('icon', 'icon-voted', downvoteId)
                replaceClass('icon-voted', 'icon', upvoteId)
                document.getElementById('votes-' + post_id).innerHTML = data.votes;
            }
            if (data.status === 'Not Authorized') {
                window.location.href = data.link;
            }
            else {
                replaceClass('icon-voted', 'icon', downvoteId)
                document.getElementById('votes-' + post_id).innerHTML = data.votes;
            }
        });
    }

    commentReply = function (id) {
        var el = document.getElementById('reply-id-' + id);
        var display = el.style.display;
        if (display === "" || display === "none") {
            el.style.display = "block";
        }
        else {
            el.style.display = "none";
        }
    }

    commentUpvote = function (comment_id) {
        data = {
            comment_id: comment_id
        }
        fetch('/comment_upvote', {
            method: 'post',
            body: JSON.stringify(data),
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            upvoteId = 'comment-upvote-' + comment_id;
            downvoteId = 'comment-downvote-' + comment_id;
            if (data.value === 1) {
                replaceClass('vote-icon', 'icon-voted', upvoteId)
                replaceClass('icon-voted', 'vote-icon', downvoteId)
                document.getElementById('comment-votes-' + comment_id).innerHTML = data.votes + " points";
            }
            if (data.status === 'Not Authorized') {
                window.location.href = data.link;
            }
            else {
                replaceClass('icon-voted', 'vote-icon', upvoteId)
                document.getElementById('comment-votes-' + comment_id).innerHTML = data.votes + " points";
            }
        });
    }

    commentDownvote = function (comment_id) {
        data = {
            comment_id: comment_id
        }
        fetch('/comment_downvote', {
            method: 'post',
            body: JSON.stringify(data),
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            upvoteId = 'comment-upvote-' + comment_id;
            downvoteId = 'comment-downvote-' + comment_id;
            if (data.value === 1) {
                replaceClass('vote-icon', 'icon-voted', downvoteId)
                replaceClass('icon-voted', 'vote-icon', upvoteId)
                document.getElementById('comment-votes-' + comment_id).innerHTML = data.votes + " points";
            }
            if (data.status === 'Not Authorized') {
                window.location.href = data.link;
            }
            else {
                replaceClass('icon-voted', 'vote-icon', downvoteId)
                document.getElementById('comment-votes-' + comment_id).innerHTML = data.votes + " points";
            }
        });
    }


});

