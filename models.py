from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(60), nullable=False)
    theme = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    end_date = db.Column(db.String(20), nullable=True)
    task_desc = db.Column(db.Text, nullable=True)