import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


def success_response(body, code=200):
    return json.dumps(body), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here
@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    return success_response(DB.get_all_users())


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    name = body.get("name")
    if name is None:
        return failure_response("Name required")
    username = body.get("username")
    if username is None:
        return failure_response("Username required")
    balance = body.get("balance")
    if balance is None:
        balance = 0
    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("Something went wrong while creating a user")
    return success_response(user, 201)


@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found")
    return success_response(user)


@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user by id
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found")
    DB.delete_user_by_id(user_id)
    return success_response(user)


@app.route("/api/send/", methods=["POST"])
def send_money():
    """
    Endpoint for sending money from one user to another
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    if sender_id is None:
        return failure_response("Sender ID required")
    receiver_id = body.get("receiver_id")
    if receiver_id is None:
        return failure_response("Receiver ID required")
    amount = body.get("amount")
    if amount is None:
        return failure_response("Amount required")
    sender = DB.get_user_by_id(sender_id)
    if sender is None:
        return failure_response("Sender not found")
    receiver = DB.get_user_by_id(receiver_id)
    if receiver is None:
        return failure_response("Receiver not found")
    if amount > sender["balance"]:
        return failure_response("Cannot send amount greater than balance", 400)
    DB.send_money_by_id(sender_id, receiver_id, amount)
    return success_response(
        {"sender_id": sender_id, "receiver_id": receiver_id, "amount": amount}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
