from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy() #initialization

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
