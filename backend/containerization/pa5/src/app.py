import json

from db import db
from flask import Flask, request
from db import Course, User, Assignment

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    # db.drop_all()
    db.create_all()


# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# your routes here
@app.route("/")
@app.route("/api/courses/")
def get_courses():
    """
    Endpoint for getting all courses
    """
    courses = [c.serialize() for c in Course.query.all()]
    return success_response(courses)


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Endpoint for creating a new course
    """
    body = json.loads(request.data)
    code = body.get("code")
    if code is None:
        return failure_response("Code required", 400)
    name = body.get("name")
    if name is None:
        return failure_response("Name required", 400)
    new_course = Course(code=code, name=name)
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)


@app.route("/api/courses/<int:course_id>/")
def get_course(course_id):
    """
    Endpoint for getting a course by id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    Endpoint for deleting a course by id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    name = body.get("name")
    if name is None:
        return failure_response("Name required", 400)
    netid = body.get("netid")
    if netid is None:
        return failure_response("Net ID required", 400)
    new_user = User(name=name, netid=netid)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize())


@app.route("/api/users/<int:user_id>")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())


@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Endpoint for adding a user to a course by id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    body = json.loads(request.data)
    user_id = body.get("user_id")
    if user_id is None:
        return failure_response("User ID required", 400)
    type = body.get("type")
    if type is None:
        return failure_response("Type required", 400)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    if user in course.students or user in course.instructors:
        return failure_response("User is already in the course")
    if type == "student":
        course.students.append(user)
    elif type == "instructor":
        course.instructors.append(user)
    else:
        return failure_response("Invalid type")
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment_for_course(course_id):
    """
    Endpoint for creating an assignment for a course by id
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found", 400)
    body = json.loads(request.data)
    title = body.get("title")
    if title is None:
        return failure_response("Title required", 400)
    due_date = body.get("due_date")
    if due_date is None:
        return failure_response("Due date required", 400)
    new_assignment = Assignment(title=title, due_date=due_date, course_id=course_id)
    db.session.add(new_assignment)
    db.session.commit()
    return success_response(new_assignment.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
