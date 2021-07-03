# core/views.py

from myproject.models import Task
from flask import render_template,request,Blueprint

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page =request.args.get('page',1,type=int)
    tasks= Task.query.order_by(Task.period).paginate(page=page, per_page=10)
    return render_template('index.html', tasks=tasks)

@core.route('/info')
def info():
    return render_template('info.html')
