from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from db import db
from models.models import LoginForm, MasterProduct, User
from utils import bcrypt

main_bp = Blueprint('main', __name__)


### LOGIN

@main_bp.route('/login', methods = ['GET', 'POST'])
def login():
     form = LoginForm()
     if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()#check if user is in the database
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(('/'))
        else:
            flash('Invalid username or password')

     return render_template('/main/login.html', form=form)

@main_bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


### MAIN MENU
@main_bp.route('/', methods =['POST', 'GET'])
@login_required
def index():
       if current_user.is_authenticated and current_user.username == 'admin':
           return render_template('/main/index.html')
       else:
            logout_user()
            flash('You do not have permission to access this page')
            return redirect(url_for('main.login'))
       
#######################################################################################
### MASTER PRODUCT ROUTE AKA PRODUCTS IN WAREHOUSE

@main_bp.route('/mastertable')
@login_required
def masterlist():
    if not current_user.is_authenticated or current_user.username != 'admin':
        logout_user()
        flash('You do not have permission to access this page')
        return redirect(url_for('main.login'))
    
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