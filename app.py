import os
from flask import Flask, render_template, redirect, request, url_for
from forms import AddTask, UpdateTask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 


app = Flask(__name__)

app.config['SECRET_KEY']='mykey'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_NOTIFICATION']=False 

db = SQLAlchemy(app)
Migrate(app,db)


######################
#Models
######################


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    period  = db.Column(db.Text,  server_default='')
    task = db.Column(db.Text(250))
    status = db.Column(db.Text, nullable=False, server_default='ToDo')

    def __init__(self, period, task, status):
        self.period = period
        self.task = task
        self.status = status


####################
#View Function
####################

@app.route('/')
def index():

    tasks = Task.query.order_by(Task.period).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET','POST'])
def add_task():

    form = AddTask()

    if form.validate_on_submit():
        period = form.period.data
        task = form.task.data
        status = form.status.data
        new_task = Task(period, task, status)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add.html', form=form)


@app.route('/update/<int:id>', methods =['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)
    form = UpdateTask(request.form, obj=task)
    

    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        return redirect(url_for('index'))
        
    
    return render_template('update.html', form=form , task = task)

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    task = Task.query.get_or_404(id)
    form = UpdateTask(request.form, obj=task)

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run()
