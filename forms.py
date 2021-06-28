from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField

class AddTask(FlaskForm):

    period = SelectField(u'Period: ', choices = [('30','30'),('60','60'),('90','90')])
    task = StringField('Plan: ')
    status = SelectField(u'Status: ', choices = [('ToDo', 'ToDo'),('InProcess','InProcess'),('Completed','Completed')])
    submit=SubmitField('Add')

class UpdateTask(FlaskForm):

    period = SelectField(u'Period: ', choices = [('30','30'),('60','60'),('90','90')])
    task = StringField('Plan: ')
    status = SelectField(u'Status: ', choices = [('ToDo', 'ToDo'),('InProcess','InProcess'),('Completed','Completed')])
    submit=SubmitField('Update')

class DeleteTask(FlaskForm):

    period = SelectField(u'Period: ', choices = [('30','30'),('60','60'),('90','90')])
    task = StringField('Plan: ')
    status = SelectField(u'Status: ', choices = [('ToDo', 'ToDo'),('InProcess','InProcess'),('Completed','Completed')])
    submit=SubmitField('Delete')