from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Task
from db import DB

# initiate a flask aplication and sqlalchemy database
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
DB.init_app(app)

@app.route('/new_task',methods=['POST'])
def new_task():
    data = request.json
    add_task = Task(
        task_name = data['task_name'],
        theme = data['theme'],
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
    'task_desc':task.task_desc,
    'start_date':task.start_date,
    'end_date':task.end_date,
    } for task in all_tasks ])

@app.route('/update_task/<int:id>',methods=['PUT'])
def update_task(id):
    data = request.json
    task = Task.query.get(id)
    if task:
        task.task_name = data.get('task_name', task.task_name)
        task.theme = data.get('theme', task.theme)
        task.task_desc = data.get('task_desc', task.task_desc)
        task.status = data.get('status', task.status)
        if task.status == False and data.get('status') == True:
            task.end_date = None
        elif task.status == True and data.get('status') == False:
            return jsonify({"message":"ERROR - to first close the task"}),400

        DB.session.commit()
        return jsonify({"message":"Task updated successfully!"}),200
    else:
        return jsonify({"message":"Task not found!"}),404
    











@app.route('/',methods=['GET'])
def main_page():
    return jsonify({'message':'Flask run'}),200

# starting point of the flask server
if __name__ == '__main__':
    with app.app_context():
        DB.create_all()
    app.run(debug=True,port=5001)