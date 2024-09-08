from flask import Flask, redirect, render_template, request, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from routes.main_routes import main_bp
from routes.dispatch_routes import dispatch_bp
from routes.order_routes import order_bp
from routes.ldn_routes import ldn_bp
from routes.esp_routes import esp_bp
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u467cpb39hfrqn:pc1030a52b519ffacdfdc3e8ee269635940660610a91806035f698bed947e3433@c8lj070d5ubs83.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddvl4j1obuhd43'
db.init_app(app)


app.register_blueprint(main_bp)
app.register_blueprint(dispatch_bp)
app.register_blueprint(order_bp)
app.register_blueprint(ldn_bp)
app.register_blueprint(esp_bp)



def __repr__(self):
           return '<Task %r>' % self.id




if __name__ == "__main__":    
    
     app.run(debug=True, port=8000)
