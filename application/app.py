from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app=Flask(__name__)

    #configurations
    #initialization
    #integration
    #usage

    from application.config import Config
    app.config.from_object(Config)

    from application.models.model import db  
    db.init_app(app)

    app.app_context().push()

    db.create_all()

    return app


