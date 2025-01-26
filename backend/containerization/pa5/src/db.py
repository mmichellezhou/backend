from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

student_association_table = db.Table("student_assocation", db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

instructor_association_table = db.Table("instructor_assocation", db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

# your classes here
class Course(db.Model):
    """
    Course model
    """
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship("Assignment", cascade="delete")
    instructors = db.relationship("User", secondary=instructor_association_table, back_populates="taught_courses")
    students = db.relationship("User", secondary=student_association_table, back_populates="enrolled_courses")

    def __init__(self, **kwargs):
        """
        Initialize course object
        """
        self.code = kwargs.get("code")
        self.name = kwargs.get("name")

    def serialize(self):
        """
        Serialize course object
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.simple_serialize() for a in self.assignments],
            "instructors": [i.simple_serialize() for i in self.instructors],
            "students": [s.simple_serialize() for s in self.students]
        }
    
    def simple_serialize(self):
        """
        Simple serialize course object
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }
    
class User(db.Model):
    """
    User model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    enrolled_courses = db.relationship("Course", secondary=student_association_table)
    taught_courses = db.relationship("Course", secondary=instructor_association_table)


    def __init__(self, **kwargs):
        """
        Initialize user object
        """
        self.name = kwargs.get("name")
        self.netid = kwargs.get("netid")

    def serialize(self):
        """
        Serialize user object
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [c.simple_serialize() for c in (self.enrolled_courses + self.taught_courses)]
        }
    
    def simple_serialize(self):
        """
        Simple serialize user object
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
        }
    
class Assignment(db.Model):
    """
    Assignment model
    """
    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    course = db.relationship("Course", back_populates="assignments")

    def __init__(self, **kwargs):
        """
        Initialize assignment object
        """
        self.title = kwargs.get("title")
        self.due_date = kwargs.get("due_date")
        self.course_id = kwargs.get("course_id")

    def serialize(self):
        """
        Serialize assignment object
        """
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course": self.course.simple_serialize()
        }
    
    def simple_serialize(self):
        """
        Simple serialize assignment object
        """
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date
        }

    