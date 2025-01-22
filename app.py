import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Task
from db import DB

# initiate a flask aplication and sqlalchemy database
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
DB.init_app(app)

@app.route('/new_task',methods=['POST'])
def new_task():
    data = request.json
    add_task = Task(
        task_name = data['task_name'],
        theme = data['theme'],
        status = 'In_progress',
        task_desc = data['task_desc'],
    )
    DB.session.add(add_task)
    DB.session.commit()
    return jsonify({'message':'task added'}),201

@app.route('/show_tasks',methods=['GET'])
def show_tasks():
    all_tasks = Task.query.all()
    return jsonify([{
    'id':task.id,
    'task_name':task.task_name,
    'theme':task.theme,
    'status':task.status,
    'start_date':task.start_date,
    'end_date':task.end_date,
    'task_desc':task.task_desc
    } for task in all_tasks ])

@app.route('/',methods=['GET'])
def main_page():
    return jsonify({'message':'Flask run'}),200

# starting point of the flask server
if __name__ == '__main__':
    with app.app_context():
        DB.create_all()
    app.run(debug=True,port=5001)