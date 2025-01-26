from datetime import datetime
import json

import db
from flask import Flask
from flask import request

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
    return success_response({"users: ": DB.get_all_users()})


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    name = body.get("name")
    if name is None:
        return failure_response("Name required", 400)
    username = body.get("username")
    if username is None:
        return failure_response("Username required", 400)
    balance = body.get("balance")
    if balance is None:
        balance = 0
    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("Something went wrong while creating a user")
    user["transactions"] = []
    return success_response(user, 201)


@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found")
    user["transactions"] = DB.get_transactions_by_user_id(user_id)
    return success_response(user)


@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user by id
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found")
    DB.delete_user_by_id(user_id)
    return success_response(user)


@app.route("/api/transactions/", methods=["POST"])
def create_transaction():
    """
    Endpoint for creating a new transaction
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    if sender_id is None:
        return failure_response("Sender ID required", 400)
    receiver_id = body.get("receiver_id")
    if receiver_id is None:
        return failure_response("Receiver ID required", 400)
    amount = body.get("amount")
    if amount is None:
        return failure_response("Amount required", 400)
    message = body.get("message")
    if message is None:
        return failure_response("Message required", 400)
    accepted = body.get("accepted")
    sender = DB.get_user_by_id(sender_id)
    if sender is None:
        return failure_response("Sender not found")
    receiver = DB.get_user_by_id(receiver_id)
    if receiver is None:
        return failure_response("Receiver not found")
    if accepted:
        if not send_money(sender_id, receiver_id, amount):
            return failure_response("Cannot send amount greater than balance", 403)
    timestamp = datetime.now().isoformat(sep=" ", timespec="microseconds")
    transaction_id = DB.insert_transaction_table(
        timestamp, sender_id, receiver_id, amount, message, accepted
    )
    transaction = DB.get_transaction_by_id(transaction_id)
    if transaction is None:
        return failure_response("Something went wrong while creating a transaction")
    return success_response(transaction)


@app.route("/api/transactions/<int:txn_id>", methods=["POST"])
def accept_or_deny_request(txn_id):
    """
    Endpoint for accepting or denying a request transaction by id
    """
    body = json.loads(request.data)
    new_accepted = body.get("accepted")
    if new_accepted is None:
        return failure_response("Accepted required", 400)
    transaction = DB.get_transaction_by_id(txn_id)
    old_accepted = transaction["accepted"]
    if old_accepted is None:
        if new_accepted:
            sender_id = transaction["sender_id"]
            receiver_id = transaction["receiver_id"]
            amount = transaction["amount"]
            if not send_money(sender_id, receiver_id, amount):
                return failure_response("Cannot send amount greater than balance", 403)
            transaction["accepted"] = True
        else:
            transaction["accepted"] = False
        timestamp = datetime.now().isoformat(sep=" ", timespec="microseconds")
        DB.accept_or_deny_request(txn_id, timestamp, new_accepted)
        transaction = DB.get_transaction_by_id(txn_id)
        return success_response(transaction)
    else:
        return failure_response("Transaction has already been accepted or denied", 403)


def send_money(sender_id, receiver_id, amount):
    """
    Helper method for sending money from one user to another by id
    """
    sender = DB.get_user_by_id(sender_id)
    if amount > sender["balance"]:
        return False
    DB.send_money_by_id(sender_id, receiver_id, amount)
    return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
