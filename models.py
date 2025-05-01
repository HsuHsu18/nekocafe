from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    categoryid = db.Column(db.ForeignKey('product_types.id'), nullable=False)
    category = db.relationship("ProductTypes", backref=db.backref("menu_items", lazy=True))

    def __str__(self):
        return f"{self.name} / {self.price} / {self.categoryid} / {self.description} / {self.image_url}"

@dataclass
class BasketItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    menu_item = db.relationship("MenuItem")

@dataclass
class ProductTypes(db.Model):
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __str__(self):
        return f"{self.category} / {self.description}"
