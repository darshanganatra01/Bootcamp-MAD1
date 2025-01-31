from flask import Blueprint,Flask,render_template,request,redirect,url_for
from application.models.model import db

bp = Blueprint('main', __name__)


@bp.route('/')
def default():
    return render_template("landing.html")
    

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    if request.method=='POST':
        first_name=request.form.get('Fname')
        last_name=request.form.get('Lname')
        print(first_name)
        print(last_name)
        return redirect('/dashboard/'+first_name)
    
@bp.route('/dashboard/<first_name>',methods=['GET','POST'])
def dashboard(first_name):
    if request.method=='GET':
        return render_template("Dashboard.html",first_name=first_name)
    

@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template("register.html")
    else:
        name = request.form.get('name')
        password = request.form.get("password")
        print(name,password)
        



    

    

#methods are the list of methods only allowed methods to the server