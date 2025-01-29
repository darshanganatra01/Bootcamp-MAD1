from application.app import create_app
from application.controllers.routes import bp

app=create_app()

app.register_blueprint(bp) #registering the routes

if __name__=='__main__':
    app.run(debug=True)

#127.0.0.1(localhost):5000(default port for flask)