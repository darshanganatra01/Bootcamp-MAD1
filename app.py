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
        first_name=request.form.get('name')
        password=request.form.get('password')
        print(first_name)
        userexist = User.query.filter_by(name=first_name).first()
        
        #then will check the password
        if userexist is None:
            print("user doesnt exist")
            return redirect('/register')
        
        else:
            if userexist.password==password:
                return redirect('/dashboard/'+str(userexist.id))
            else:
                return "password doesnt match"
            #we will learn how to use flash msgs
    
    
    
@app.route('/dashboard/<id>',methods=['GET','POST'])
def dashboard(id):
    if request.method=='GET':
        userdetails=User.query.filter_by(id=int(id)).first()
        return render_template("Dashboard.html",userdetails=userdetails)
    

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        name = request.form.get('name')
        password = request.form.get('password')

        #creating and instance 
        print(name,password)


        new_user = User(name=name,password=password)
        #L.H.S is what name is the name in the database
        #R.H.S the name you want to give

        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/login')
    
    
@app.route('/all_users',methods=['GET'])
def all_users():
    users = User.query.all()  #list of all objects of the table(Every entry is an object of user class) 
    print(users)

    userfirst=User.query.filter_by(name='Darshan').first()
    #give me the first user whose name is darshan

    userall=User.query.filter_by(name="Darshan").all()
    #give me all the users whose name is darshan 

    return render_template("all_users.html",userfirst=userfirst,userall=userall)



@app.route('/update/<id>',methods=['GET','POST'])
def update(id):
    if request.method=='GET':
        return render_template("update.html")
    else:
        new_name=request.form.get('name')
        new_password=request.form.get('password')

    userthatiwanttoupdate = User.query.filter_by(id=id).first()

    userthatiwanttoupdate.name = new_name
    userthatiwanttoupdate.password = new_password

    db.session.commit()
    return redirect('/dashboard/'+str(userthatiwanttoupdate.id))





@app.route('/delete/<id>')
def delete(id):
    userthatiwanttodelete =  User.query.filter_by(id=id).first()
    db.session.delete(userthatiwanttodelete)
    db.session.commit()
    return "Deleted the user successfullty"

















    

    







#methods are the list of methods only allowed methods to the server


        




if __name__=='__main__':
    app.run(debug=True)



#127.0.0.1(localhost):5000(default port for flask)