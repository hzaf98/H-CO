from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models.models import MasterProduct

main_bp = Blueprint('main', __name__)

### MAIN MENU
@main_bp.route('/', methods =['POST', 'GET'])
def index():
    
       return render_template('/main/index.html')
#######################################################################################
### MASTER PRODUCT ROUTE AKA PRODUCTS IN WAREHOUSE

@main_bp.route('/mastertable')
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

@main_bp.route('/deletemaster/<int:id>')
def delete3(id):
    product_to_delete = MasterProduct.query.get_or_404(id)#Attempts to get import by id and if it doesnt exist it will 404

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/mastertable')
    except:
        return 'There was an issue deleting the product'


#######################################################################################