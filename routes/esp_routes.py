from flask import Blueprint, app, render_template, request, redirect, url_for
from db import db
from models.models import EspDispOrder, EspDispatchedProduct, MasterProduct

esp_bp = Blueprint('esp', __name__)

### ESP DISPATCHES
@esp_bp.route('/espform', methods = ['POST', 'GET'])
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
    
@esp_bp.route('/esplist')
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
@esp_bp.route('/espdeletedisp/<int:id>')
def espdelete(id):
    dispatches_to_delete = EspDispOrder.query.get_or_404(id)#Attempts to get import by id and if it doesnt exist it will 404

    try:
        db.session.delete(dispatches_to_delete)
        db.session.commit()
        return redirect('/esplist')
    except:
        return 'There was an issue deleting the dispatch'