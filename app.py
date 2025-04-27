from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Link to your SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nekocafe.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy()
db.init_app(app)

# Menu item model
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.String(200))
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(100))  # e.g. images/3.png
    carbon_impact = db.Column(db.Float)

@app.route('/')
def index():
    menu_items = MenuItem.query.all()
    return render_template('index.html', menu_items=menu_items)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create all tables if they don't exist
    app.run(debug=True)
