import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {
        "id": 0,
        "upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98",
    },
    1: {
        "id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98",
    },
}

comments_lists = {
    0: {
        0: {
            "id": 0,
            "upvotes": 8,
            "text": "Wow, my first Reddit gold!",
            "username": "alicia98",
        }
    },
    1: {},
}


pid_counter = 2
cid_counter = 1


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here
@app.route("/api/posts/")
def get_posts():
    """
    Returns all posts
    """
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200


@app.route("/api/posts/", methods=["POST"])
def create_post():
    """
    Creates a new post
    """
    global pid_counter
    body = json.loads(request.data)
    title = body.get("title")
    if title is None:
        return json.dumps({"error": "Title required"}), 400
    link = body.get("link")
    if link is None:
        return json.dumps({"error": "Link required"}), 400
    username = body.get("username")
    if username is None:
        return json.dumps({"error": "Username required"}), 400
    post = {
        "id": pid_counter,
        "upvotes": 1,
        "title": title,
        "link": link,
        "username": username,
    }
    posts[pid_counter] = post
    comments_lists[pid_counter] = {}
    pid_counter += 1
    return json.dumps(post), 201


@app.route("/api/posts/<int:pid>/")
def get_post(pid):
    """
    Gets the post with id, pid
    """
    post = posts.get(pid)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    return json.dumps(post), 200


@app.route("/api/posts/<int:pid>/", methods=["DELETE"])
def delete_post(pid):
    """
    Deletes the post with id, pid
    """
    post = posts.get(pid)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    del posts[pid]
    del comments_lists[pid]
    return json.dumps(post), 200


@app.route("/api/posts/<int:pid>/comments/")
def get_comments(pid):
    """
    Returns all comments for the post with id, pid
    """
    comments = comments_lists.get(pid)
    if comments is None:
        return json.dumps({"error": "Post not found"}), 404
    res = {"comments": list(comments.values())}
    return json.dumps(res), 200


@app.route("/api/posts/<int:pid>/comments/", methods=["POST"])
def post_comment(pid):
    """
    Posts a new comment for the post with id, pid
    """
    global cid_counter
    body = json.loads(request.data)
    text = body.get("text")
    if text is None:
        return json.dumps({"error": "Text required"}), 400
    username = body.get("username")
    if username is None:
        return json.dumps({"error": "Username required"}), 400
    comment = {"id": cid_counter, "upvotes": 1, "text": text, "username": username}
    comments = comments_lists.get(pid)
    if comments is None:
        return json.dumps({"error": "Post not found"}), 404
    comments[cid_counter] = comment
    cid_counter += 1
    return json.dumps(comment), 201


@app.route("/api/posts/<int:pid>/comments/<int:cid>/", methods=["POST"])
def edit_comment(pid, cid):
    """
    Edits the comment with id, cid, for the post with id, pid
    """
    body = json.loads(request.data)
    text = body.get("text")
    if text is None:
        return json.dumps({"error": "Text required"}), 400
    comments = comments_lists.get(pid)
    if comments is None:
        return json.dumps({"error": "Post not found"}), 404
    comment = comments[cid]
    if comment is None:
        return json.dumps({"error": "Comment not found"}), 404
    comment["text"] = text
    return json.dumps(comment), 200


@app.route("/api/extra/posts/", methods=["POST"])
def extra_create_post():
    """
    Creates a new post
    """
    global pid_counter
    body = json.loads(request.data)
    title = body.get("title")
    if title is None:
        return json.dumps({"error": "Title required"}), 400
    elif not isinstance(title, str):
        return json.dumps({"error": "Title must be of type <str>"}), 400
    link = body.get("link")
    if link is None:
        return json.dumps({"error": "Link required"}), 400
    elif not isinstance(link, str):
        return json.dumps({"error": "Link must be of type <str>"}), 400
    username = body.get("username")
    if username is None:
        return json.dumps({"error": "Username required"}), 400
    elif not isinstance(username, str):
        return json.dumps({"error": "Username must be of type <str>"}), 400
    post = {
        "id": pid_counter,
        "upvotes": 1,
        "title": title,
        "link": link,
        "username": username,
    }
    posts[pid_counter] = post
    comments_lists[pid_counter] = {}
    pid_counter += 1
    return json.dumps(post), 201


@app.route("/api/extra/posts/<int:pid>/comments/", methods=["POST"])
def extra_post_comment(pid):
    """
    Posts a new comment for the post with id, pid
    """
    global cid_counter
    body = json.loads(request.data)
    text = body.get("text")
    if text is None:
        return json.dumps({"error": "Text required"}), 400
    elif not isinstance(text, str):
        return json.dumps({"error": "Text must be of type <str>"}), 400
    username = body.get("username")
    if username is None:
        return json.dumps({"error": "Username required"}), 400
    elif not isinstance(username, str):
        return json.dumps({"error": "Username must be of type <str>"}), 400
    comment = {"id": cid_counter, "upvotes": 1, "text": text, "username": username}
    comments = comments_lists.get(pid)
    if comments is None:
        return json.dumps({"error": "Post not found"}), 404
    comments[cid_counter] = comment
    cid_counter += 1
    return json.dumps(comment), 201


@app.route("/api/extra/posts/<int:pid>/comments/<int:cid>/", methods=["POST"])
def extra_edit_comment(pid, cid):
    """
    Edits the comment with id, cid, for the post with id, pid
    """
    body = json.loads(request.data)
    text = body.get("text")
    if text is None:
        return json.dumps({"error": "Text required"}), 400
    elif not isinstance(text, str):
        return json.dumps({"error": "Text must be of type <str>"}), 400
    comments = comments_lists.get(pid)
    if comments is None:
        return json.dumps({"error": "Post not found"}), 404
    comment = comments[cid]
    if comment is None:
        return json.dumps({"error": "Comment not found"}), 404
    comment["text"] = text
    return json.dumps(comment), 200


@app.route("/api/posts/<int:pid>/", methods=["POST"])
def upvote_post(pid):
    """
    Upvotes the post with id, pid
    """
    post = posts.get(pid)
    if post is None:
        return json.dumps({"error": "Post not found"}), 404
    if request.data:
        body = json.loads(request.data)
        upvotes = body.get("upvotes")
        if upvotes is None:
            upvotes = 1
        elif not isinstance(upvotes, int):
            return json.dumps({"error": "Upvotes must be of type <int>"}), 400
    else:
        upvotes = 1
    post["upvotes"] += upvotes
    return json.dumps(post), 200


@app.route("/api/extra/posts/")
def extra_get_posts():
    """
    Returns all posts
    """
    value = request.args.get("sort")
    sorted_posts = posts
    if value == "increasing":
        sorted_posts = dict(sorted(posts.items(), key=lambda item: item[1]["upvotes"]))
        print("increasing sorted: " + str(sorted_posts))
    elif value == "decreasing":
        sorted_posts = dict(sorted(posts.items(), key=lambda item: item[1]["upvotes"], reverse=True))
        print("decreasing sorted: " + str(sorted_posts))
    res = {"posts": list(sorted_posts.values())}
    return json.dumps(res), 200
    

@app.route("/<path:subpath>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(subpath):
    """
    Catch-all route
    """
    return json.dumps({"error": "Invalid route"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
