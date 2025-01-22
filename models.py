from db import DB
from datetime import datetime, timezone

class Task(DB.Model):
    __tablename__ = 'tasks'

    id = DB.Column(DB.Integer, primary_key=True)
    task_name = DB.Column(DB.String(60), nullable=False)
    theme = DB.Column(DB.String(10), nullable=False)
    status = DB.Column(DB.String(20), nullable=False)
    task_desc = DB.Column(DB.Text, nullable=True)
    start_date = DB.Column(DB.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    end_date = DB.Column(DB.String(20), nullable=True)

