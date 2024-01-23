from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"
    serialize_rules = ('-restaurants.pizza',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    ingredients = db.Column(db.String, nullable=False)

    restaurants = db.relationship(
        'RestaurantPizza', back_populates='pizza')

    def __repr__(self):
        return f"<Pizza id:{self.id}, name:{self.name}>"


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"
    serialize_rules = ('-pizzas.restaurant',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)

    pizzas = db.relationship(
        'RestaurantPizza', back_populates='restaurant')

    def __repr__(self):
        return f"<Restaurant id:{self.id}, name:{self.name}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizza"
    serialize_rules = ('-pizza.restaurants',
                       '-restaurant.pizzas')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    pizza = db.relationship('Pizza', back_populates='restaurants')
    restaurant = db.relationship(
        'Restaurant', back_populates='pizzas')

    @validates('price')
    def validate_price(self, key, price):
        if 1 <= price <= 30:
            return price
        raise ValueError('price should range between 1 and 30')

    def __repr__(self):
        return f"<RestaurantPizza id:{self.id}, res:{self.restaurant_id}, pizza:{self.pizza_id}>"