from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from models import db, MenuItem, BasketItem, ProductTypes

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

# Route to display menu
@app.route('/')
def index():
    menu_items_py = MenuItem.query.all()  # Fetch all menu items
    print(menu_items_py)  # Debugging line to check the fetched items
    product_types = ProductTypes.query.all()  # Fetch all product types
    return render_template('index.html', menu_items = menu_items_py, product_types=product_types)

# Add item to the basket
@app.route('/add_to_basket/<int:item_id>')
def add_to_basket(item_id):
    item = MenuItem.query.get(item_id)
    if 'basket' not in session:
        session['basket'] = []

    # Add the item to the basket (we store item details in the basket)
    session['basket'].append({
        'id': item.id,
        'name': item.name,
        'price': item.price,
        'image_url': item.image_url
    })

    session.modified = True
    return redirect(url_for('view_basket'))

# View the basket
@app.route('/basket')
def view_basket():
    basket_items = session.get('basket', [])
    total_price = sum(item['price'] for item in basket_items)
    return render_template('basket.html', basket_items=basket_items, total_price=total_price)

# Checkout (placeholder route)
@app.route('/checkout')
def checkout():
    basket_items = session.get('basket', [])
    total_price = sum(item['price'] for item in basket_items)
    return render_template('checkout.html', basket_items=basket_items, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
