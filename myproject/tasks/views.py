from flask import render_template,url_for,flash, redirect,request, Blueprint, abort
from flask_login import current_user,login_required
from myproject import db
from myproject.models import Task
from myproject.tasks.forms import AddTask

tasks = Blueprint('tasks',__name__)

@tasks.route('/create',methods=['GET','POST'])
@login_required
def add_task():
    form = AddTask()
    
    if form.validate_on_submit():

        task = Task(period=form.period.data,
                             task=form.task.data,
                             status=form.status.data,
                             user_id=current_user.id
                             )
        db.session.add(task)
        db.session.commit()
        flash("Plan Added")
        return redirect(url_for('users.user_tasks', username = current_user.username))

    return render_template('add_task.html',form=form)


# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
'''@tasks.route('/<int:task_id>')
def task(task_id):
    # grab the requested blog post by id number or return 404
    task = Task.query.get_or_404(task_id)
    return render_template('task.html',period=task.period, task=task, status=task.status)'''


@tasks.route("/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = AddTask()

    if form.validate_on_submit():
        task.period = form.period.data
        task.task = form.task.data
        task.status = form.status.data

        db.session.commit()
        flash('Task Updated')
        return redirect(url_for('users.user_tasks', username = current_user.username))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.period.data = task.period
        form.task.data = task.task
        form.status.data = task.status

    return render_template('add_task.html', title='Update',
                           form=form)


@tasks.route("/<int:task_id>/delete", methods=['GET','POST'])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
       abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('users.user_tasks', username = current_user.username))
