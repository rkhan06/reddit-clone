$(document).ready(function () {
    replaceClass = function(oldClass, newClass, id){
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
            document.getElementById('votes-'+post_id).innerHTML = data.votes;
            upvoteId = 'upvote-' + post_id;
            downvoteId = 'downvote-' + post_id;
            if (data.value === 1) {
                replaceClass('icon', 'icon-voted', upvoteId)
                replaceClass('icon-voted', 'icon', downvoteId)

            } else {
                replaceClass('icon-voted', 'icon', upvoteId)
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
            document.getElementById('votes-'+post_id).innerHTML = data.votes;
            downvoteId = 'downvote-' + post_id;
            upvoteId = 'upvote-' + post_id;
            if (data.value === 1) {
                replaceClass('icon', 'icon-voted', downvoteId)
                replaceClass('icon-voted', 'icon', upvoteId)
            } else {
                replaceClass('icon-voted', 'icon', downvoteId)
            }
        });
    }

    commentReply = function(id){
        var el = document.getElementById('reply-id-' + id );
        var display = el.style.display;
        if(display === "" || display === "none"){
            el.style.display = "block";
        }
        else{
            el.style.display = "none";
        }
    }


});

