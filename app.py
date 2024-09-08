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

    def __repr__(self):
           return '<Task %r>' % self.id

### MAIN MENU
@app.route('/', methods =['POST', 'GET'])
def index():
    
       return render_template('/main/index.html')
#######################################################################################
### MASTER PRODUCT ROUTE AKA PRODUCTS IN WAREHOUSE

@app.route('/mastertable')
def masterlist():

    page = int(request.args.get('page', 1))  # Get the current page number from the URL
    per_page = 14  # Number of items to display per page
       
    q = request.args.get('q')  # Get the search query from the URL
    
    if q:
            masterslist_paginated = MasterProduct.query.filter(
                (MasterProduct.product_name.like('%' + q + '%')) 
                
                
               
                # Add more fields to search here
            ).order_by(MasterProduct.date_created).paginate(per_page=14, page=page, error_out=False)
    else:
         masterslist_paginated = MasterProduct.query.order_by(MasterProduct.date_created.desc()).paginate(per_page=14, page=page, error_out=False)

    masterslist = masterslist_paginated.items  # Get the list of imports for the current page

    return render_template('/main/mastertable.html', masterslist = masterslist, pagination = masterslist_paginated)

@app.route('/deletemaster/<int:id>')
def delete3(id):
    product_to_delete = MasterProduct.query.get_or_404(id)#Attempts to get import by id and if it doesnt exist it will 404

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/main/mastertable')
    except:
        return 'There was an issue deleting the product'


#######################################################################################

### CREATE AN ORDER RECEIVED
@app.route('/received', methods = ['POST', 'GET'])
def createform1():
    if request.method == 'POST': #If post, put the values into DB, else look at page.
        products = request.form.getlist('product[]')
        suppliers = request.form.getlist('supplier[]')
        pallets = request.form.getlist('pallet[]')
        cartons = request.form.getlist('carton[]')
        packs = request.form.getlist('pack[]')
        weights = request.form.getlist('weight[]')
        locations = request.form.getlist('location[]')
        arrival = request.form['arrival']

        new_order = OrderR(arrival=arrival)
        db.session.add(new_order)
        db.session.flush()  # Get the ID of the newly created OrderR instance

        for product, supplier, pallet, carton, pack, weight, location in zip(products, suppliers, pallets, cartons, packs, weights, locations):
            # Check if the product already exists in the MasterProduct table
            master_product = MasterProduct.query.filter_by(product_name=product,supplier=supplier).first()
            if master_product:
                # If the product and supplier exists, add the pallet quantity
                master_product.total_pallets += int(pallet)
                master_product.total_cartons = int(carton)
                master_product.total_pack = int(pack)
                master_product.total_weight = int(weight)

            else:
                # If the product doesn't exist, create a new MasterProduct instance
                master_product = MasterProduct(product_name=product,supplier=supplier, location= location, total_pallets=int(pallet), total_cartons=int(carton), total_pack=int(pack), total_weight=int(weight))
                db.session.add(master_product)

            # Create a new OrderRProduct instance for each product
            order_product = OrderRProduct(order_id=new_order.id,location=location, product_name=product, supplier=supplier, pallets=int(pallet), cartons=int(carton), weight=int(weight), pack=int(pack) )
            db.session.add(order_product)
        
        try:
            db.session.commit()
            return redirect('/received')
        except:
            return 'There was an issue adding your order'

    else:
     return render_template('/main/received.html')

### ORDERS RECEIVED LIST
@app.route('/receivedlist')
def orderslist():
    page = int(request.args.get('page', 1))  # Get the current page number from the URL
    per_page = 13  # Number of items to display per page
       
    q = request.args.get('q')  # Get the search query from the URL
    
    if q:
            orders_paginated = OrderR.query.filter(
                (OrderR.product_name.like('%' + q + '%')) |
                (OrderR.arrival.like('%' + q + '%')) |
                (OrderR.supplier.like('%' + q + '%')) 
                
               
                # Add more fields to search here
            ).order_by(OrderR.date_created).paginate(per_page=13, page=page, error_out=False)
    else:
         orders_paginated = OrderR.query.order_by(OrderR.date_created.desc()).paginate(per_page=13, page=page, error_out=False)

    orders = orders_paginated.items  # Get the list of imports for the current page

    return render_template('/main/receivedlist.html', orders = orders, pagination = orders_paginated)

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
    order_products = OrderRProduct.query.filter_by(order_id=orders.id).all()
    
    if request.method == 'POST':
        orders.arrival = request.form['arrival']

        products = request.form.getlist('product[]')
        suppliers = request.form.getlist('supplier[]')
        pallets = request.form.getlist('pallet[]')
        cartons = request.form.getlist('carton[]')
        packs = request.form.getlist('pack[]')
        weights = request.form.getlist('weight[]')
        locations = request.form.getlist('location[]')

        #Sending to products table
        for i, (product, supplier, pallet, carton, pack, weight, location) in enumerate(zip(products, suppliers, pallets, cartons, packs, weights, locations)):
            order_product = order_products[i]
            order_product.product_name = product
            order_product.supplier = supplier
            order_product.pallets = int(pallet)
            order_product.cartons = int(carton)
            order_product.pack = int(pack)
            order_product.weight = int(weight)
            order_product.location = location
            
            master_product = MasterProduct.query.filter_by(product_name=product,supplier=supplier).first()
            
            if master_product:
                # If the product and supplier exists, add the pallet quantity and all other details
                master_product.total_pallets += int(pallet)
                master_product.total_cartons = int(carton)
                master_product.total_pack = int(pack)
                master_product.total_weight = int(weight)
                master_product.location = location

            else:
                # If the product doesn't exist, create a new MasterProduct instance
                master_product = MasterProduct(product_name=product,supplier=supplier, total_pallets=int(pallet), total_cartons=int(carton), total_pack=int(pack), total_weight=int(weight), location = location)
                db.session.add(master_product)


        try:
            db.session.commit()
            return redirect('receivedlist')
        except:
            return 'There was an issue updating the list'
        
    else:

         return render_template('/main/recupdate.html', orders = orders, order_products = order_products)
    
###########################################################################################

### CREATE DISPATCHED ORDER FORM

@app.route('/dispatchedform', methods = ['POST', 'GET'])
def createform2():
    if request.method == 'POST': #If post, put the values into DB, else look at page.
        products = request.form.getlist('product[]')
        suppliers = request.form.getlist('supplier[]')
        pallets = request.form.getlist('pallets[]')
        cartons = request.form.getlist('carton[]')
        packs = request.form.getlist('pack[]')
        weights = request.form.getlist('weight[]')
        dispatch_date = request.form['dispatch_date']
        dispatch_time = request.form['dispatch_time']
        collected = request.form['collected']
        delivered = request.form['delivered']
        recipient = request.form['recipient']
        delivery_add = request.form['delivery_add']
        collector = request.form['collector']
        vehicle = request.form['vehicle']
        signature = request.form['signature']
        verified_by = request.form['verified_by']
        verified_date = request.form['verified_date']

        new_dispatch = DispOrder(dispatch_date = dispatch_date, dispatch_time = dispatch_time, collected = collected, delivered = delivered, recipient = recipient, delivery_add = delivery_add, collector = collector,vehicle = vehicle, signature = signature, verified_by = verified_by, verified_date = verified_date )
        db.session.add(new_dispatch)
        db.session.flush()  # Get the ID of the newly created DispOrder instance
        
        for product, supplier, pallet, carton, pack, weight in zip(products, suppliers, pallets, cartons, packs, weights):
        # Check if the product already exists in the MasterProduct table
            master_product = MasterProduct.query.filter_by(product_name=product, supplier = supplier).first()
            if master_product:
                # If the product exists, minus the quantity from the total quantity
                master_product.total_pallets -= int(pallet)
                master_product.total_cartons = int(carton)
                master_product.total_pack = int(pack)
                master_product.total_weight = int(weight)


            # Create a new DispatchedProduct instance for each product
            order_product = DispatchedProduct(dispatch_id=new_dispatch.id, product_name=product, supplier = supplier, pallets_sent=int(pallet), cartons_sent=int(carton), pack_sent=int(pack), weight_sent=int(weight))
            db.session.add(order_product)
        
        try:
           
            db.session.commit()
            return redirect('/dispatchedform')
        except:
            return 'There was an issue adding your order'

    else:
     return render_template('/main/dispatchedform.html')

### DISPATCHED ORDERS LIST

@app.route('/dispatchedlist')
def dispatchedlist():
    page = int(request.args.get('page', 1))  # Get the current page number from the URL
    per_page = 13  # Number of items to display per page
       
    q = request.args.get('q')  # Get the search query from the URL
    
    if q:
            dispatches_paginated = DispOrder.query.filter(
                (DispOrder.product_name.like('%' + q + '%')) 
                
                
               
                # Add more fields to search here
            ).order_by(DispOrder.date_created).paginate(per_page=13, page=page, error_out=False)
    else:
         dispatches_paginated = DispOrder.query.order_by(DispOrder.date_created.desc()).paginate(per_page=13, page=page, error_out=False)

    dispatches = dispatches_paginated.items  # Get the list of imports for the current page

    return render_template('/main/dispatchedlist.html', dispatches = dispatches, pagination = dispatches_paginated)

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
    dispatched_products = DispatchedProduct.query.filter_by(dispatch_id=dispatches.id).all()

    if request.method == 'POST': #If post, put the values into DB, else look at page.
        dispatches.dispatch_date = request.form['dispatch_date']
        dispatches.dispatch_time = request.form['dispatch_time']
        dispatches.collected = request.form['collected']
        dispatches.delivered = request.form['delivered']
        dispatches.recipient = request.form['recipient']
        dispatches.delivery_add = request.form['delivery_add']
        dispatches.collector = request.form['collector']
        dispatches.vehicle = request.form['vehicle']
        dispatches.signature = request.form['signature']
        dispatches.verified_by = request.form['verified_by']
        dispatches.verified_date = request.form['verified_date']
        
        products = request.form.getlist('product[]')
        suppliers = request.form.getlist('supplier[]')
        pallets = request.form.getlist('pallets[]')
        cartons = request.form.getlist('carton[]')
        packs = request.form.getlist('pack[]')
        weights = request.form.getlist('weight[]')

        for i, (product, supplier, pallet, carton, pack, weight) in enumerate(zip(products, suppliers, pallets, cartons, packs, weights)):
            dispatched_product = dispatched_products[i]
            dispatched_product.product_name = product
            dispatched_product.supplier = supplier
            dispatched_product.pallets_sent = int(pallet)
            dispatched_product.cartons_sent = int(carton)
            dispatched_product.pack_sent = int(pack)
            dispatched_product.weight_sent = int(weight)

            master_product = MasterProduct.query.filter_by(product_name=product, supplier=supplier).first()
            
            if master_product:
                # If the product exists, minus the quantity from the total quantity
                master_product.total_pallets -= int(pallet)
                master_product.total_cartons = int(carton)
                master_product.total_pack = int(pack)
                master_product.total_weight = int(weight)

     


        try:
            db.session.commit()
            return redirect('/dispatchedlist')
        
        except:
            return 'There was an issue updating the list'
            
    else:

        return render_template('/main/dispupdate.html', dispatches = dispatches, dispatched_products = dispatched_products)
    
### LDN DISPATCHES
@app.route('/ldnform', methods = ['POST', 'GET'])
def ldnform():
    if request.method == 'POST': #If post, put the values into DB, else look at page.
        products = request.form.getlist('product[]')
        suppliers = request.form.getlist('supplier[]')
        pallets = request.form.getlist('pallets[]')
        cartons = request.form.getlist('carton[]')
        packs = request.form.getlist('pack[]')
        weights = request.form.getlist('weight[]')
        dispatch_date = request.form['dispatch_date']
        dispatch_time = request.form['dispatch_time']
        collected = request.form['collected']
        delivered = request.form['delivered']
        recipient = request.form['recipient']
        delivery_add = request.form['delivery_add']
        collector = request.form['collector']
        vehicle = request.form['vehicle']
        signature = request.form['signature']
        verified_by = request.form['verified_by']
        verified_date = request.form['verified_date']

        new_dispatch = LdnDispOrder(dispatch_date = dispatch_date, dispatch_time = dispatch_time, collected = collected, delivered = delivered, recipient = recipient, delivery_add = delivery_add, collector = collector,vehicle = vehicle, signature = signature, verified_by = verified_by, verified_date = verified_date )
        db.session.add(new_dispatch)
        db.session.flush()  # Get the ID of the newly created DispOrder instance
        
        for product, supplier, pallet, carton, pack, weight in zip(products, suppliers, pallets, cartons, packs, weights):
        # Check if the product already exists in the MasterProduct table
            master_product = MasterProduct.query.filter_by(product_name=product, supplier = supplier).first()
            if master_product:
                # If the product exists, minus the quantity from the total quantity
                master_product.total_pallets -= int(pallet)
                master_product.total_cartons = int(carton)
                master_product.total_pack = int(pack)
                master_product.total_weight = int(weight)


            # Create a new DispatchedProduct instance for each product
            order_product = LdnDispatchedProduct(dispatch_id=new_dispatch.id, product_name=product, supplier = supplier, pallets_sent=int(pallet), cartons_sent=int(carton), pack_sent=int(pack), weight_sent=int(weight))
            db.session.add(order_product)
        
        try:
           
            db.session.commit()
            return redirect('/ldnform')
        except:
            return 'There was an issue adding your order'

    else:
     return render_template('/ldn/ldnform.html')
    
@app.route('/ldnlist')
def ldnlist():
    page = int(request.args.get('page', 1))  # Get the current page number from the URL
    per_page = 13  # Number of items to display per page
       
    q = request.args.get('q')  # Get the search query from the URL
    
    if q:
            dispatches_paginated = LdnDispOrder.query.filter(
                (LdnDispOrder.product_name.like('%' + q + '%')) 
                
                
               
                # Add more fields to search here
            ).order_by(LdnDispOrder.date_created).paginate(per_page=13, page=page, error_out=False)
    else:
         dispatches_paginated = LdnDispOrder.query.order_by(LdnDispOrder.date_created.desc()).paginate(per_page=13, page=page, error_out=False)

    dispatches = dispatches_paginated.items  # Get the list of imports for the current page

    return render_template('/ldn/ldnlist.html', dispatches = dispatches, pagination = dispatches_paginated)

### LDN DELETE DISPATCHED ORDER
@app.route('/ldndeletedisp/<int:id>')
def ldndelete(id):
    dispatches_to_delete = LdnDispOrder.query.get_or_404(id)#Attempts to get import by id and if it doesnt exist it will 404

    try:
        db.session.delete(dispatches_to_delete)
        db.session.commit()
        return redirect('/ldnlist')
    except:
        return 'There was an issue deleting the dispatch'

### ESP DISPATCHES
@app.route('/espform', methods = ['POST', 'GET'])
def espform():
    if request.method == 'POST': #If post, put the values into DB, else look at page.
        products = request.form.getlist('product[]')
        suppliers = request.form.getlist('supplier[]')
        pallets = request.form.getlist('pallets[]')
        cartons = request.form.getlist('carton[]')
        packs = request.form.getlist('pack[]')
        weights = request.form.getlist('weight[]')
        dispatch_date = request.form['dispatch_date']
        dispatch_time = request.form['dispatch_time']
        collected = request.form['collected']
        delivered = request.form['delivered']
        recipient = request.form['recipient']
        delivery_add = request.form['delivery_add']
        collector = request.form['collector']
        vehicle = request.form['vehicle']
        signature = request.form['signature']
        verified_by = request.form['verified_by']
        verified_date = request.form['verified_date']

        new_dispatch = EspDispOrder(dispatch_date = dispatch_date, dispatch_time = dispatch_time, collected = collected, delivered = delivered, recipient = recipient, delivery_add = delivery_add, collector = collector,vehicle = vehicle, signature = signature, verified_by = verified_by, verified_date = verified_date )
        db.session.add(new_dispatch)
        db.session.flush()  # Get the ID of the newly created DispOrder instance
        
        for product, supplier, pallet, carton, pack, weight in zip(products, suppliers, pallets, cartons, packs, weights):
        # Check if the product already exists in the MasterProduct table
            master_product = MasterProduct.query.filter_by(product_name=product, supplier = supplier).first()
            if master_product:
                # If the product exists, minus the quantity from the total quantity
                master_product.total_pallets -= int(pallet)
                master_product.total_cartons = int(carton)
                master_product.total_pack = int(pack)
                master_product.total_weight = int(weight)


            # Create a new DispatchedProduct instance for each product
            order_product = EspDispatchedProduct(dispatch_id=new_dispatch.id, product_name=product, supplier = supplier, pallets_sent=int(pallet), cartons_sent=int(carton), pack_sent=int(pack), weight_sent=int(weight))
            db.session.add(order_product)
        
        try:
           
            db.session.commit()
            return redirect('/espform')
        except:
            return 'There was an issue adding your order'

    else:
     return render_template('/esp/espform.html')
    
@app.route('/esplist')
def esplist():
    page = int(request.args.get('page', 1))  # Get the current page number from the URL
    per_page = 13  # Number of items to display per page
       
    q = request.args.get('q')  # Get the search query from the URL
    
    if q:
            dispatches_paginated = EspDispOrder.query.filter(
                (EspDispOrder.product_name.like('%' + q + '%')) 
                
                
               
                # Add more fields to search here
            ).order_by(EspDispOrder.date_created).paginate(per_page=13, page=page, error_out=False)
    else:
         dispatches_paginated = EspDispOrder.query.order_by(EspDispOrder.date_created.desc()).paginate(per_page=13, page=page, error_out=False)

    dispatches = dispatches_paginated.items  # Get the list of imports for the current page

    return render_template('/esp/esplist.html', dispatches = dispatches, pagination = dispatches_paginated)

### LDN DELETE DISPATCHED ORDER
@app.route('/espdeletedisp/<int:id>')
def espdelete(id):
    dispatches_to_delete = EspDispOrder.query.get_or_404(id)#Attempts to get import by id and if it doesnt exist it will 404

    try:
        db.session.delete(dispatches_to_delete)
        db.session.commit()
        return redirect('/esplist')
    except:
        return 'There was an issue deleting the dispatch'
if __name__ == "__main__":    
    
     app.run(debug=True, port=8000)
