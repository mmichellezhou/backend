import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


# generalized response formats
def success_response(body, code=200):
    return json.dumps(body), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/")
@app.route("/tasks/")
def get_tasks():
    """
    Endpoint for getting all tasks
    """
    return success_response({"tasks": DB.get_all_tasks()})


@app.route("/tasks/", methods=["POST"])
def create_task():
    """
    Endpoint for creating a new task
    """
    body = json.loads(request.data)
    description = body.get("description")
    task_id = DB.insert_task_table(description, False)
    task = DB.get_task_by_id(task_id)
    if task is None:
        return failure_response("Could not create task.", 400)
    return success_response(task, 201)


@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    """
    Endpoint for getting a task by id
    """
    task = DB.get_task_by_id(task_id)
    if task is None:
        return failure_response("Task not found!")
    task["subtasks"] = DB.get_subtasks_of_task(task_id)
    return success_response(task)


@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    """
    Endpoint for updating a task by id
    """
    body = json.loads(request.data)
    description = body.get("description")
    done = body.get("done")
    DB.update_task_by_id(task_id, description, done)

    task = DB.get_task_by_id(task_id)
    if task is None:
        return failure_response("Task not found!")
    return success_response(task)


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    """
    Endpoint for deleting a task by id
    """
    task = DB.get_task_by_id(task_id)
    if task is None:
        return failure_response("Task not found!")
    DB.delete_task_by_id(task_id)
    return success_response(task)


@app.route("/task/<int:task_id>/subtasks/", methods=["POST"])
def create_subtask(task_id):
    body = json.loads(request.data)
    description = body.get("description")
    if description is None:
        return failure_response("Description required")
    try:
        subtask = {
            "id": DB.insert_subtask(description, False, task_id),
            "description": description,
            "done": False,
            "task_id": task_id,
        }
        return json.dumps({"success": True, "data": subtask})
    except sqlite3.IntegrityError:
        return json.dumps({"success": False, "error": "Task not found"}), 404


@app.route("/task/<int:task_id>/subtasks/")
def get_subtasks_of_task(task_id):
    res = {"subtasks": DB.get_subtasks_of_task(task_id)}
    return json.dumps(res), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
