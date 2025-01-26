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
@app.route("/tasks/")
def get_tasks():
    return success_response(DB.get_all_tasks())


@app.route("/tasks/", methods=["POST"])
def create_task():
    body = json.loads(request.data)
    description = body.get("description")
    if description is None:
        return failure_response("Description required")
    # demo: description = body["description"], but this may raise an error
    task_id = DB.insert_task_table(description, False)
    task = DB.get_task_by_id(task_id)
    if task is None:
        return failure_response("Something went wrong while creating a task")
    return success_response(task, 201)


@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = DB.get_task_by_id(task_id)
    if task is None:
        return failure_response("Task not found")
    return success_response(task)


@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    body = json.loads(request.data)
    description = body.get("description")
    if description is None:
        return failure_response("Description required")
    # demo: description = body["description"], but this may raise an error
    done = body.get("done")
    if done is None:
        return failure_response("Done required")
    # demo: done = body["done"], but this may raise an error
    DB.update_task_by_id(task_id, description, done)
    task = DB.get_task_by_id(task_id)
    if task is None:
        return failure_response("Task not found")
    return success_response(task)


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    task = DB.get_task_by_id(task_id)
    if task is None:
        return failure_response("Task not found")
    DB.delete_task_by_id(task_id)
    return success_response(task)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
