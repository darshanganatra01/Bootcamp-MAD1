from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)

#configurations
#initialization
#integration
#usage


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3' #configuration

db=SQLAlchemy() #initialization

db.init_app(app) #integration

app.app_context().push()

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)

class Role(db.Model):
    __tablename__='role'
    role_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    role_name=db.Column(db.String,nullable=False)

class RoleUsers(db.Model):
    __tablename__='role_users'
    rel_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    rid=db.Column(db.Integer,db.ForeignKey(Role.role_id),nullable=False)
    uid=db.Column(db.Integer,db.ForeignKey(User.id),nullable=False)


db.create_all() 
#this is only for creating th einstance folder and database but if it already exists then i wil
#have to do flask migration



@app.route('/')
def default():
    return render_template("landing.html")
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    if request.method=='POST':
        first_name=request.form.get('Fname')
        last_name=request.form.get('Lname')
        print(first_name)
        print(last_name)
        return redirect('/dashboard/'+first_name)
    
@app.route('/dashboard/<first_name>',methods=['GET','POST'])
def dashboard(first_name):
    if request.method=='GET':
        return render_template("Dashboard.html",first_name=first_name)
    


    

    







#methods are the list of methods only allowed methods to the server


        




if __name__=='__main__':
    app.run(debug=True)



#127.0.0.1(localhost):5000(default port for flask)