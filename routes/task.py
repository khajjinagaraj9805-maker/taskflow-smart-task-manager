from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import current_user, login_required
from models import db, Task

import pandas as pd
import numpy as np

from extensions import socketio

task_bp = Blueprint('task', __name__)


# ================= DASHBOARD =================

@task_bp.route('/dashboard')
@login_required
def dashboard():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    task_data = []

    for task in tasks:

        task_data.append({
            "title": task.title,
            "status": task.status
        })

    df = pd.DataFrame(task_data)

    total = len(df)

    completed = np.sum(
        df["status"] == "Completed"
    ) if total > 0 else 0

    pending = np.sum(
        df["status"] == "Pending"
    ) if total > 0 else 0

    completion_percentage = round(
        (completed / total) * 100,
        2
    ) if total > 0 else 0

    analytics = {
        "total": int(total),
        "completed": int(completed),
        "pending": int(pending),
        "completion_percentage": completion_percentage
    }

    return render_template(
        'dashboard.html',
        tasks=tasks,
        analytics=analytics,
        user=current_user
    )


# ================= ADD TASK =================

@task_bp.route('/add_task', methods=['POST'])
@login_required
def add_task():

    task = Task(
        title=request.form['title'],
        description=request.form['description'],
        priority=request.form['priority'],
        status=request.form['status'],
        user_id=current_user.id
    )

    db.session.add(task)

    db.session.commit()

    # ================= SOCKET NOTIFICATION =================

    socketio.emit(
        'task_notification',
        {
            'message': f'✅ New Task Added: {task.title}'
        }
    )

    return redirect('/dashboard')


# ================= EDIT TASK =================

@task_bp.route('/edit_task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    if request.method == 'POST':

        task.title = request.form['title']

        task.description = request.form['description']

        task.priority = request.form['priority']

        task.status = request.form['status']

        db.session.commit()

        socketio.emit(
            'task_notification',
            {
                'message': f'✏️ Task Updated: {task.title}'
            }
        )

        return redirect('/dashboard')

    return render_template(
        'edit_task.html',
        task=task
    )


# ================= DELETE TASK =================

@task_bp.route('/delete_task/<int:id>')
@login_required
def delete_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    socketio.emit(
        'task_notification',
        {
            'message': f'❌ Task Deleted: {task.title}'
        }
    )

    db.session.delete(task)

    db.session.commit()

    return redirect('/dashboard')


# ================= GET TASKS API =================

@task_bp.route('/api/tasks')
@login_required
def get_tasks():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    data = []

    for task in tasks:

        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "created_date": task.created_date
        })

    return jsonify(data)


# ================= ADD TASK API =================

@task_bp.route('/api/add_task', methods=['POST'])
@login_required
def api_add_task():

    data = request.json

    task = Task(
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        status=data['status'],
        user_id=current_user.id
    )

    db.session.add(task)

    db.session.commit()

    socketio.emit(
        'task_notification',
        {
            'message': f'✅ API Task Added: {task.title}'
        }
    )

    return jsonify({
        "message": "Task Added Successfully"
    })


# ================= UPDATE TASK API =================

@task_bp.route('/api/update_task/<int:id>', methods=['PUT'])
@login_required
def api_update_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    data = request.json

    task.title = data['title']

    task.description = data['description']

    task.priority = data['priority']

    task.status = data['status']

    db.session.commit()

    socketio.emit(
        'task_notification',
        {
            'message': f'✏️ API Task Updated: {task.title}'
        }
    )

    return jsonify({
        "message": "Task Updated Successfully"
    })


# ================= DELETE TASK API =================

@task_bp.route('/api/delete_task/<int:id>', methods=['DELETE'])
@login_required
def api_delete_task(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    socketio.emit(
        'task_notification',
        {
            'message': f'❌ API Task Deleted: {task.title}'
        }
    )

    db.session.delete(task)

    db.session.commit()

    return jsonify({
        "message": "Task Deleted Successfully"
    })