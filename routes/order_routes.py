from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from db import db
from models.models import MasterProduct, OrderR, OrderRProduct

order_bp = Blueprint('order', __name__)
### CREATE AN ORDER RECEIVED
@order_bp.route('/received', methods = ['POST', 'GET'])
@login_required
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
@order_bp.route('/receivedlist')
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
@order_bp.route('/deleteor/<int:id>')
def delete(id):
    order_to_delete = OrderR.query.get_or_404(id)#Attempts to get import by id and if it doesnt exist it will 404

    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        return redirect('/receivedlist')
    except:
        return 'There was an issue deleting the order'


### ORDERS RECEIVED UPDATE PAGE
@order_bp.route('/recupdate/<int:id>', methods=['GET', 'POST'])
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
            return redirect('/receivedlist')
        except:
            return 'There was an issue updating the list'
        
    else:

         return render_template('/main/recupdate.html', orders = orders, order_products = order_products)
    
###########################################################################################