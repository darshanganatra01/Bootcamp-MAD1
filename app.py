from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)

#configurations
#initialization
#integration
#usage


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3' #configuration
app.config['SECRET_KEY']='saltedpepper'

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

class Album(db.Model):   #1 MYFAV   #2 DRIVE
    __tablename__='album'
    alb_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    album_name=db.Column(db.String,nullable=False)
    #userkey foreign

class Songs(db.Model):
    __tablename__='songs'
    s_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_name=db.Column(db.String,nullable=False)
    foreign_album=db.Column(db.ForeignKey(Album.alb_id),nullable=False) #1

    album=db.relationship(Album,backref=db.backref('songs'))
    #back_populates


#relationship is object to object
#<Song 1>.album  =====> <Album 1> extract names and anything
#<Album 1> =====> <Song 3> <Song 4>  extracr everything



#add some new table lets say playist
#if i will run the app again it will not show the changes
#you will lose the data that you saved in the database when doing this 
#whenever you update the database you should use flask_migration so that you can update
#the database without deleting the database and keep your old data safe



#<Songs 1>
#song.album <Album 1>




db.create_all() 
#this is only for creating th einstance folder and database but if it already exists then i wil
#have to do flask migration

#you will have to check that if there is someone named admin in the database 
#and it has a role of admin

#User object -----> role -----> admin



 


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
        albums=Album.query.all()
        songs=Songs.query.all()
        return render_template("Dashboard.html",userdetails=userdetails,songs=songs,albums=albums)
    

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


@app.route('/add_album/<id>',methods=['GET','POST'])
def add_album(id):
    if request.method=='GET':
        return render_template('add_album.html')
    else:
        albumname=request.form.get('albumname')
        ifalbumalreadyexist=Album.query.filter_by(album_name=albumname).first()
        if ifalbumalreadyexist:
            return "Album already exists use some different name"
        else:
            albumiwanttoadd = Album(album_name=albumname)
            db.session.add(albumiwanttoadd)
            db.session.commit()
            return redirect('/add_song/'+id)
        

@app.route('/add_song/<id>',methods=['GET','POST'])
def add_song(id):
    if request.method=='GET':
        all_albums=Album.query.all()
        return render_template('add_song.html',all_albums=all_albums,userid=id)
    else:
        songname=request.form.get('songname')
        select_album=request.form.get('select_album')
        ifsongalreadyexist=Songs.query.filter_by(song_name=songname).first()
        if ifsongalreadyexist:
            flash("song already exists")
            return redirect('/add_song/'+id)
        else:
            songiwanttoadd = Songs(song_name=songname,foreign_album=select_album)
            db.session.add(songiwanttoadd)
            db.session.commit()
            return redirect('/dashboard/'+id)
        
@app.route('/songofthatalbems/<id>')
def songs(id):
    #realtionships are object to object 
    #i have the album id now i will find the object of that album id thencall
    #songs relationship on that id

    album_instance=Album.query.filter_by(alb_id=id).first()
    songs=album_instance.songs
    print(songs)
    return render_template('songofalbum.html',songs=songs)


@app.route('/songpage/<id>')
def song(id):
    songinstance=Songs.query.filter_by(s_id=id).first()
    album=songinstance.album
    print(album)
    return render_template('songpage.html',songinstance=songinstance,album=album)

    
    


    




















    

    







#methods are the list of methods only allowed methods to the server


        




if __name__=='__main__':
    app.run(debug=True)



#127.0.0.1(localhost):5000(default port for flask)