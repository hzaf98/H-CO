from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u467cpb39hfrqn:pc1030a52b519ffacdfdc3e8ee269635940660610a91806035f698bed947e3433@c8lj070d5ubs83.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddvl4j1obuhd43'
db = SQLAlchemy(app)

class DispOrder(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      date_created = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
      dispatch_date = db.Column(db.String)
      dispatch_time = db.Column(db.String)
      collected = db.Column(db.String)
      delivered = db.Column(db.String)
      product = db.Column(db.String)
      quantity = db.Column(db.String)
      recipient = db.Column(db.String)
      delivery_add = db.Column(db.String)
      collector = db.Column(db.String)
      vehicle = db.Column(db.String)
      signature = db.Column(db.String)
      verified_by = db.Column(db.String)
      verified_date = db.Column(db.String)
   


### ORDERS RECEIVED DB TABLE
class OrderR(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      product= db.Column(db.String)
      quantity = db.Column(db.String)
      arrival = db.Column(db.String)
      supplier = db.Column(db.String)
      date_created = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

     
      def __repr__(self):
           return '<Task %r>' % self.id

### MAIN MENU
@app.route('/', methods =['POST', 'GET'])
def index():
    
       return render_template('index.html')
#######################################################################################

### CREATE AN ORDER RECEIVED
@app.route('/received', methods = ['POST', 'GET'])
def createform1():
    if request.method == 'POST': #If post, put the values into DB, else look at page.
        product = request.form['product']
        quantity = request.form['quantity']
        arrival = request.form['arrival']
        supplier = request.form['supplier']
    
        new_order = OrderR(product = product, quantity = quantity, arrival = arrival, supplier = supplier)
        
        try:
            db.session.add(new_order)
            db.session.commit()
            return redirect('/received')
        except:
            return 'There was an issue adding your order'

    else:
     return render_template('received.html')

### ORDERS RECEIVED LIST
@app.route('/receivedlist')
def orderslist():
    page = int(request.args.get('page', 1))  # Get the current page number from the URL
    per_page = 10  # Number of items to display per page
       
    q = request.args.get('q')  # Get the search query from the URL
    
    if q:
            orders_paginated = OrderR.query.filter(
                (OrderR.product.like('%' + q + '%')) |
                (OrderR.quantity.like('%' + q + '%')) |
                (OrderR.arrival.like('%' + q + '%')) |
                (OrderR.supplier.like('%' + q + '%')) 
                
               
                # Add more fields to search here
            ).order_by(OrderR.date_created).paginate(per_page=10, page=page, error_out=False)
    else:
         orders_paginated = OrderR.query.order_by(OrderR.date_created).paginate(per_page=10, page=page, error_out=False)

    orders = orders_paginated.items  # Get the list of imports for the current page

    return render_template('receivedlist.html', orders = orders, pagination = orders_paginated)

### ORDERS RECEIVED LIST PAGE DEL
@app.route('/deleteor/<int:id>')
def delete(id):
    order_to_delete = OrderR.query.get_or_404(id)#Attempts to get import by id and if it doesnt exist it will 404

    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        return redirect('/receivedlist')
    except:
        return 'There was an issue deleting the order'


### ORDERS RECEIVED UPDATE PAGE
@app.route('/recupdate/<int:id>', methods=['GET', 'POST'])
def editform1(id):
    orders = OrderR.query.get_or_404(id)
    
    if request.method == 'POST':
        orders.product = request.form['product']
        orders.quantity = request.form['arrival']
        orders.arrival = request.form['product']
        orders.supplier = request.form['supplier']

        try:
            db.session.commit()
            return redirect('/receivedlist')
        except:
            return 'There was an issue updating the list'
        
    else:

         return render_template('recupdate.html', orders = orders)
    
###########################################################################################

### CREATE DISPATCHED ORDER FORM

@app.route('/dispatchedform', methods = ['POST', 'GET'])
def createform2():
    if request.method == 'POST': #If post, put the values into DB, else look at page.
        dispatch_date = request.form['dispatch_date']
        dispatch_time = request.form['dispatch_time']
        collected = request.form['collected']
        delivered = request.form['delivered']
        product = request.form['product']
        quantity = request.form['quantity']
        recipient = request.form['recipient']
        delivery_add = request.form['delivery_add']
        collector = request.form['collector']
        vehicle = request.form['vehicle']
        signature = request.form['signature']
        verified_by = request.form['verified_by']
        verified_date = request.form['verified_date']

        new_dispatch = DispOrder(dispatch_date = dispatch_date, dispatch_time = dispatch_time, collected = collected, delivered = delivered,  product =  product, quantity = quantity, recipient = recipient, delivery_add = delivery_add, collector = collector,vehicle = vehicle, signature = signature, verified_by = verified_by, verified_date = verified_date )
        
        try:
            db.session.add(new_dispatch)
            db.session.commit()
            return redirect('/dispatchedform')
        except:
            return 'There was an issue adding your order'

    else:
     return render_template('dispatchedform.html')

### DISPATCHED ORDERS LIST

@app.route('/dispatchedlist')
def dispatchedlist():
    page = int(request.args.get('page', 1))  # Get the current page number from the URL
    per_page = 10  # Number of items to display per page
       
    q = request.args.get('q')  # Get the search query from the URL
    
    if q:
            dispatches_paginated = DispOrder.query.filter(
                (DispOrder.product.like('%' + q + '%')) |
                (DispOrder.quantity.like('%' + q + '%')) |
                (DispOrder.arrival.like('%' + q + '%')) 
                
               
                # Add more fields to search here
            ).order_by(DispOrder.date_created).paginate(per_page=10, page=page, error_out=False)
    else:
         dispatches_paginated = DispOrder.query.order_by(DispOrder.date_created).paginate(per_page=10, page=page, error_out=False)

    dispatches = dispatches_paginated.items  # Get the list of imports for the current page

    return render_template('dispatchedlist.html', dispatches = dispatches, pagination = dispatches_paginated)

### DELETE DISPATCHED ORDER

@app.route('/deletedisp/<int:id>')
def delete2(id):
    dispatches_to_delete = DispOrder.query.get_or_404(id)#Attempts to get import by id and if it doesnt exist it will 404

    try:
        db.session.delete(dispatches_to_delete)
        db.session.commit()
        return redirect('/dispatchedlist')
    except:
        return 'There was an issue deleting the dispatch'

### UPDATE DISPATCHED ORDER

@app.route('/dispupdate/<int:id>', methods=['GET', 'POST'])
def editform2(id):
    dispatches = DispOrder.query.get_or_404(id)

    if request.method == 'POST': #If post, put the values into DB, else look at page.
            dispatches.dispatch_date = request.form['dispatch_date']
            dispatches.dispatch_time = request.form['dispatch_time']
            dispatches.collected = request.form['collected']
            dispatches.delivered = request.form['delivered']
            dispatches.product = request.form['product']
            dispatches.quantity = request.form['quantity']
            dispatches.recipient = request.form['recipient']
            dispatches.delivery_add = request.form['delivery_add']
            dispatches.collector = request.form['collector']
            dispatches.vehicle = request.form['vehicle']
            dispatches.signature = request.form['signature']
            dispatches.verified_by = request.form['verified_by']
            dispatches.verified_date = request.form['verified_date']
          
            
            try:
                db.session.commit()
                return redirect('/dispatchedlist')
            
            except:
                return 'There was an issue updating the list'
            
    else:
        return render_template('dispupdate.html', dispatches = dispatches)

if __name__ == "__main__":    
    
     app.run(debug=True, port=8000)
