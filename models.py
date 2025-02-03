from db import DB
from datetime import datetime, timezone

class IPAddres(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    ip_address = DB.Column(DB.String(46), nullable=False, unique=True)
    blacklist = DB.Column(DB.Boolean, default=False)
    added_at = DB.Column(DB.DateTime, default=lambda: datetime.now(timezone.utc))

class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(15), nullable=False, unique=True)
    password = DB.Column(DB.String(15), nullable=False)
    added_at = DB.Column(DB.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship with Task
    tasks = DB.relationship('Task', backref='user', lazy=True) 

class Task(DB.Model):
    __tablename__ = 'tasks'

    id = DB.Column(DB.Integer, primary_key=True) # task id ( autoincrement)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False) # the user id who creates the task
    task_name = DB.Column(DB.String(60), nullable=False) # the name of the task
    theme = DB.Column(DB.String(10), nullable=False) # the theme of the new task( work,home,school)
    status = DB.Column(DB.Boolean, default=True) # status of the task ( active or not)
    task_desc = DB.Column(DB.Text, nullable=False) # the task description
    start_date = DB.Column(DB.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)) # the date when user open the task
    end_date = DB.Column(DB.DateTime, nullable=True) # the date when user close the task
    deleted = DB.Column(DB.Boolean, default=False) # hide or show if deleted
    deleted_at = DB.Column(DB.DateTime, nullable=True) # date if deleting the task

    def to_dict(self):
        """Translate the SQL to dict ."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def from_dict(self,data):
        """Translate the dict to SQL."""
        for field in data:
            if hasattr(self, field):  # Only set attributes that exist on the model
                setattr(self, field, data[field])

