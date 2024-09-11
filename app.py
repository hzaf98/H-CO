from flask import Flask, redirect, render_template, request, url_for, Blueprint
from datetime import datetime
from models.models import User
from routes.main_routes import main_bp
from routes.dispatch_routes import dispatch_bp
from routes.order_routes import order_bp
from routes.ldn_routes import ldn_bp
from routes.esp_routes import esp_bp
from db import db
from utils import bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u467cpb39hfrqn:pc1030a52b519ffacdfdc3e8ee269635940660610a91806035f698bed947e3433@c8lj070d5ubs83.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddvl4j1obuhd43'
app.config['SECRET_KEY'] = 'secretkey'
db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

app.register_blueprint(main_bp)
app.register_blueprint(dispatch_bp)
app.register_blueprint(order_bp)
app.register_blueprint(ldn_bp)
app.register_blueprint(esp_bp)



def __repr__(self):
           return '<Task %r>' % self.id




if __name__ == "__main__":    
    
     app.run(debug=True, port=8000)
