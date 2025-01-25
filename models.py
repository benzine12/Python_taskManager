from db import DB
from datetime import datetime, timezone

class Task(DB.Model):
    __tablename__ = 'tasks'

    id = DB.Column(DB.Integer, primary_key=True) # task id ( autoincrement)
    task_name = DB.Column(DB.String(60), nullable=False) # the name of the task
    theme = DB.Column(DB.String(10), nullable=False) # the theme of the new task( work,home,school)
    status = DB.Column(DB.Boolean, default=True) # status of the task ( active or not)
    task_desc = DB.Column(DB.Text, nullable=True) # the task description
    start_date = DB.Column(DB.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)) # the date when user open the task
    end_date = DB.Column(DB.String(20), nullable=True) # the date when user close the task
    is_deleted = DB.Column(DB.Boolean, default=False) # the status of the task (deleted or not)

