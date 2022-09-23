from navigate import app
from navigate.models import *
from navigate import db
from  navigate import culc_path
@app.route('/')
def get_all_customers():  # put application's code here
   return History.query.all()

@app.route('/add_new_order')
def add_new_customer():  # put application's code here

    return 'succsee'
