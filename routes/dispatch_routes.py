from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models.models import DispOrder, DispatchedProduct, MasterProduct

dispatch_bp = Blueprint('dispatch', __name__)

### CREATE DISPATCHED ORDER FORM

@dispatch_bp.route('/dispatchedform', methods = ['POST', 'GET'])
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

@dispatch_bp.route('/dispatchedlist')
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

@dispatch_bp.route('/deletedisp/<int:id>')
def delete2(id):
    dispatches_to_delete = DispOrder.query.get_or_404(id)#Attempts to get import by id and if it doesnt exist it will 404

    try:
        db.session.delete(dispatches_to_delete)
        db.session.commit()
        return redirect('/dispatchedlist')
    except:
        return 'There was an issue deleting the dispatch'

### UPDATE DISPATCHED ORDER

@dispatch_bp.route('/dispupdate/<int:id>', methods=['GET', 'POST'])
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