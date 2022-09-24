from navigate import app
from navigate.models import *
from flask import Flask, render_template, url_for, request, redirect
from navigate import db
from  navigate import culc_path
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # task_content = request.form['content']
        # new_task = History(content=task_content)
        #
        # try:
        #     db.session.add(new_task)
        #     db.session.commit()
        #     return redirect('/')
        # except:
        #     return 'There was an issue adding your task'
        pass
    else:
        history = History.query.all()
        # return history
        return render_template('index.html', tasks=history)

@app.route('/add_new_order')
def add_new_customer():  # put application's code here

    return 'succsee'
