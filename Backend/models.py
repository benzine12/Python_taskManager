from db import DB
from datetime import datetime, timezone

class User(DB.Model):
    __tablename__ = 'users'

    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(15), nullable=False, unique=True)
    password = DB.Column(DB.String(255), nullable=False)
    added_at = DB.Column(DB.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship with Task
    tasks = DB.relationship('Task', backref='user', lazy=True) 

class Task(DB.Model):
    __tablename__ = 'tasks'

    id = DB.Column(DB.Integer, primary_key=True) # task id ( autoincrement)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'), nullable=False) # the user id who creates the task
    
    task_name = DB.Column(DB.String(60), nullable=False) # the name of the task
    theme = DB.Column(DB.String(15), nullable=False) # the theme of the new task( work,home,school)
    status = DB.Column(DB.Boolean, default=True) # status of the task ( active or not)
    task_desc = DB.Column(DB.Text, nullable=False) # the task description
    start_date = DB.Column(DB.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)) # the date when user open the task
    end_date = DB.Column(DB.DateTime, nullable=True) # the date when user close the task
    deleted = DB.Column(DB.Boolean, default=False) # hide or show if deleted
    deleted_at = DB.Column(DB.DateTime, nullable=True) # date if deleting the task

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "task_name": self.task_name,
            "theme": self.theme,
            "status": self.status,
            "task_desc": self.task_desc,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "deleted": self.deleted,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None
        }

    @classmethod
    def active(cls):
        """Return only not deleted tasks for querying."""
        return cls.query.filter_by(deleted=False)

