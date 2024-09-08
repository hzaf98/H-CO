from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from db import db



class DispOrder(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      date_created = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
      dispatch_date = db.Column(db.String)
      dispatch_time = db.Column(db.String)
      collected = db.Column(db.String)
      delivered = db.Column(db.String)
      recipient = db.Column(db.String)
      delivery_add = db.Column(db.String)
      collector = db.Column(db.String)
      vehicle = db.Column(db.String)
      signature = db.Column(db.String)
      verified_by = db.Column(db.String)
      verified_date = db.Column(db.String)
   
class DispatchedProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispatch_id = db.Column(db.Integer, db.ForeignKey('disp_order.id'))
    dispatch = db.relationship('DispOrder', backref='products')
    supplier = db.Column(db.String)
    product_name = db.Column(db.String)
    pallets_sent = db.Column(db.Integer)
    cartons_sent = db.Column(db.Integer)
    pack_sent = db.Column(db.Integer)
    weight_sent = db.Column(db.Integer)
    

### ORDERS RECEIVED DB TABLE
class OrderR(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      arrival = db.Column(db.String)
      date_created = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

class OrderRProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_r.id'))
    order = db.relationship('OrderR', backref='products')
    product_name = db.Column(db.String)
    supplier = db.Column(db.String) 
    pallets = db.Column(db.Integer)
    cartons = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    pack = db.Column(db.Integer)
    location = db.Column(db.String)

##MASTER PRODUCT AKA PRODUCTS CURRENTLY IN WAREHOUSE

class MasterProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    total_pallets = db.Column(db.Integer, default=0)
    total_cartons = db.Column(db.Integer, default=0)
    total_pack = db.Column(db.Integer, default=0)
    total_weight = db.Column(db.Integer, default=0)
    supplier = db.Column(db.String)
    location = db.Column(db.String)
    
    date_created = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

##LDNDISPATCH
class LdnDispOrder(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      date_created = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
      dispatch_date = db.Column(db.String)
      dispatch_time = db.Column(db.String)
      collected = db.Column(db.String)
      delivered = db.Column(db.String)
      recipient = db.Column(db.String)
      delivery_add = db.Column(db.String)
      collector = db.Column(db.String)
      vehicle = db.Column(db.String)
      signature = db.Column(db.String)
      verified_by = db.Column(db.String)
      verified_date = db.Column(db.String)
   
class LdnDispatchedProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispatch_id = db.Column(db.Integer, db.ForeignKey('ldn_disp_order.id'))
    dispatch = db.relationship('LdnDispOrder', backref='products')
    supplier = db.Column(db.String)
    product_name = db.Column(db.String)
    pallets_sent = db.Column(db.Integer)
    cartons_sent = db.Column(db.Integer)
    pack_sent = db.Column(db.Integer)
    weight_sent = db.Column(db.Integer)

##LDNDISPATCH
class EspDispOrder(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      date_created = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
      dispatch_date = db.Column(db.String)
      dispatch_time = db.Column(db.String)
      collected = db.Column(db.String)
      delivered = db.Column(db.String)
      recipient = db.Column(db.String)
      delivery_add = db.Column(db.String)
      collector = db.Column(db.String)
      vehicle = db.Column(db.String)
      signature = db.Column(db.String)
      verified_by = db.Column(db.String)
      verified_date = db.Column(db.String)
   
class EspDispatchedProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispatch_id = db.Column(db.Integer, db.ForeignKey('esp_disp_order.id'))
    dispatch = db.relationship('EspDispOrder', backref='products')
    supplier = db.Column(db.String)
    product_name = db.Column(db.String)
    pallets_sent = db.Column(db.Integer)
    cartons_sent = db.Column(db.Integer)
    pack_sent = db.Column(db.Integer)
    weight_sent = db.Column(db.Integer)   