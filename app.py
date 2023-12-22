import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import time

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)


@app.route('/')
def home():
    time.sleep(1)
    hint = 'task is saved successfully.'
    return render_template('index.html', hint=hint)


@app.route('/todos')
def todos():
    return render_template('todos.html')


@app.route('/api/save_task', methods=['POST'])
def save_task():

    task = request.form['task']
    count = db.tasks.count_documents({})
    task_id = count + 1

    doc = {
        'task_id': task_id,
        'task': task,
        'status': 0
    }

    db.tasks.insert_one(doc)
    return redirect(url_for('home'))


@app.route('/api/delete_task', methods=['POST'])
def delete_task():
    task_id = request.form['task_id']
    db.tasks.delete_one({'task_id': int(task_id)})
    return jsonify({'message': 'task deleted!'})


@app.route('/api/complete_task', methods=['POST'])
def complete_task():
    task_id = request.form['task_id']
    db.tasks.update_one({'task_id': int(task_id)}, {'$set': {'status': 1}})
    return jsonify({'message': 'task completed!'})


@app.route('/api/load_tasks', methods=['GET'])
def load_tasks():
    tasks = list(db.tasks.find({}, {'_id': False}))
    return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
