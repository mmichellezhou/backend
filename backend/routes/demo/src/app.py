import json
from flask import Flask
from flask import request

app = Flask(__name__)

tasks = {
    0: {"id": 0, "description": "Do the laundry", "done:": False},
    1: {"id": 1, "description": "Do the dishes", "done": False},
}

task_id_counter = 2


@app.route("/backend")
def hello():
    return "Hello!"


@app.route("/tasks/")  # GET request (default) tells server we want to retrieve data
def get_tasks():
    """
    Returns all tasks
    """
    res = {"tasks": list(tasks.values())}
    return json.dumps(res), 200  # 200 response code: data/tasks retrieved successfully


@app.route(
    "/tasks/", methods=["POST"]
)  # POST request tells server we want to manipulate data
def create_task():
    """
    Creates a new task
    """
    global task_id_counter  # to reference variable task_id_counter
    body = json.loads(request.data)
    description = body["description"]
    task = {"id": task_id_counter, "description": description, "done": False}
    tasks[task_id_counter] = task
    task_id_counter += 1
    return json.dumps(task), 201  # 201 response code: data/task created successfully


@app.route("/tasks/<int:task_id>")
def get_task(task_id):
    """
    Returns the task with id, task_id
    """
    task = tasks.get(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"}), 404
    return json.dumps(task), 200  # 200 response code: data/task retrieved successfully


@app.route("/tasks/<int:task_id>", methods=["POST"])
def update_task(task_id):
    """
    Updates the task with id, task_id
    """
    body = json.loads(request.data)
    task = tasks.get(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"}), 404
    task["description"] = body["description"]
    task["done"] = body["done"]
    return json.dumps(task), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Deletes the task with id, task_id
    """
    global task_id_counter
    task = tasks.get(task_id)
    if task is None:
        return json.dumps({"error": "Task not found"}), 404
    # delete(task_id)
    # task_id_counter -= 1
    del tasks[task_id]
    return json.dumps(task), 200


# def delete(task_id):
#     '''
#     Deletes task with id, task_id
#     '''
#     for id in range(task_id + 1, task_id_counter):
#         task = tasks[id]
#         task["id"] -= 1
#         tasks[task["id"]] = task
#     del tasks[task_id_counter - 1]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
