from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import current_user, login_required
from models import db, Task
import numpy as np

task_bp = Blueprint('task', __name__)


# ================= DASHBOARD =================

@task_bp.route('/dashboard')
@login_required
def dashboard():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    total = len(tasks)

    completed = len(
        [t for t in tasks if t.status == 'Completed']
    )

    pending = total - completed

    completion_percentage = 0

    if total > 0:

        completion_percentage = np.round(
            (completed / total) * 100,
            2
        )

    analytics = {
        "total": total,
        "completed": completed,
        "pending": pending,
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

    print(f"New Task Added: {task.title}")

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

    db.session.delete(task)

    db.session.commit()

    return redirect('/dashboard')


# ================= API =================

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
            "status": task.status
        })

    return jsonify(data)