from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from models import db, MenuItem, BasketItem, ProductTypes
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for sessions

# Link to your SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nekocafe.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
# db = SQLAlchemy()
db.init_app(app)

# class MenuItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     price = db.Column(db.Float, nullable=False)
#     image_url = db.Column(db.String(255), nullable=False)
#     category = db.Column(db.String(50)) 

with app.app_context():
    db.create_all()  # Create all tables if they don't exist

# Define the search form
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()], render_kw={"placeholder": "Search for a drink..."})
    submit = SubmitField('Search')

# Route to display menu
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    query = None
    menu_items_py = MenuItem.query.all()  # Fetch all menu items
    print(menu_items_py)  # Debugging line to check the fetched items
    product_types = ProductTypes.query.all()  # Fetch all product types
    selected_category = request.form.get('category', 'all')  # Get selected category from the form

    if form.validate_on_submit():
        query = form.search.data.lower()  # Get the search query from the form

    # Fetch all product types and filter menu items
    product_types = ProductTypes.query.all()
    if query or selected_category != 'all':
        menu_items_py = MenuItem.query.filter(
            (MenuItem.name.ilike(f"%{query}%") if query else True) &
            (MenuItem.category.has(category=selected_category) if selected_category != 'all' else True)
        ).all()
    else:
        menu_items_py = MenuItem.query.all()

    return render_template('index.html', form=form, menu_items=menu_items_py, product_types=product_types)

@app.route('/item/<int:item_id>',methods=['GET', 'POST'])
def claraNekocafe(item_id):
    item= db.get_or_404(MenuItem, item_id)
    print(item)
    return render_template('claraNekocafe.html', item=item)


@app.route('/add_to_basket/<int:item_id>')
def add_to_basket(item_id):
    # default to empty dict
    basket = session.get('basket', {})

    # if basket is not a dict (e.g., accidentally a list), reset it
    if not isinstance(basket, dict):
        basket = {}

    item_id_str = str(item_id)
    basket[item_id_str] = basket.get(item_id_str, 0) + 1

    session['basket'] = basket
    session.modified = True

    return redirect(url_for('view_basket'))

@app.route('/remove_from_basket/<int:item_id>', methods=['POST'])
def remove_from_basket(item_id):
    basket = session.get('basket', {})

    if not isinstance(basket, dict):
        basket = {}

    item_id_str = str(item_id)

    if item_id_str in basket:
        del basket[item_id_str]

    session['basket'] = basket
    session.modified = True

    return redirect(url_for('view_basket'))


@app.route('/basket')
def view_basket():
    basket = session.get('basket', {})

    if not isinstance(basket, dict):
        basket = {}

    items = []  # Initialize an empty list for items
    total = 0.0  # Initialize the total to 0

    for item_id_str, quantity in basket.items():
        item = MenuItem.query.get(int(item_id_str))
        if item:
            # Add the MenuItem object directly to the list
            item.quantity = quantity  # Add a custom attribute for quantity
            items.append(item)
            total += int(item.price) * int(quantity)

    return render_template('basket.html', items=items, total=total)

@app.context_processor
def inject_basket():
    basket = session.get('basket', {})
    if not isinstance(basket, dict):
        basket = {}

    # Get the first item in the basket (if any)
    first_item = None
    for item_id_str in basket.keys():
        first_item = MenuItem.query.get(int(item_id_str))
        if first_item:
            break

    return {'basket_first_item': first_item}

# @app.route('/remove_from_basket/<int:item_id>')
# def remove_from_basket(item_id):
#     basket = session.get('basket', {})

#     item_id_str = str(item_id)
#     if item_id_str in basket:
#         del basket[item_id_str]
#         session['basket'] = basket
#         session.modified = True

#     return redirect(url_for('view_basket'))


# # Add item to the basket
# @app.route('/add_to_basket/<int:item_id>')
# def add_to_basket(item_id):
#     item = MenuItem.query.get(item_id)
#     if 'basket' not in session:
#         session['basket'] = []

#     # Add the item to the basket (we store item details in the basket)
#     session['basket'].append({
#         'id': item.id,
#         'name': item.name,
#         'price': item.price,
#         'image_url': item.image_url
#     })

#     session.modified = True
#     return redirect(url_for('view_basket'))

# # View the basket
# @app.route('/basket')
# def view_basket():
#     basket_items = session.get('basket', [])
#     total_price = sum(item['price'] for item in basket_items)
#     return render_template('basket.html', basket_items=basket_items, total_price=total_price)

# Checkout (placeholder route)
@app.route('/checkout')
def checkout():
    basket = session.get('basket', {})

    items = []  # Initialize an empty list for items
    total = 0.0  # Initialize the total to 0

    for item_id_str, quantity in basket.items():
        item = MenuItem.query.get(int(item_id_str))
        if item:
            # Add the MenuItem object directly to the list
            item.quantity = quantity  # Add a custom attribute for quantity
            items.append(item)
            total += int(item.price) * int(quantity)

    print(basket)
    print(total)
    return render_template('checkout.html', basket_items=items, total_price=total)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5001
        )
