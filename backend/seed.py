from faker import Faker
from app import app
from models import RestaurantPizza, Restaurant, db, Pizza
from random import choice as rc, randint as ri

pizza_flavors = [
    "Margherita",
    "Pepperoni",
    "Vegetarian",
    "Hawaiian",
    "BBQ Chicken",
    "Mushroom and Olive",
    "Meat Lovers",
    "Buffalo Chicken",
    "Pesto and Tomato",
    "Four Cheese",
    "Supreme",
    "White Pizza",
    "Veggie Delight",
    "Chicken Alfredo",
    "Spinach and Feta",
    "Bacon and Onion",
    "Artichoke and Pesto",
    "Sausage and Mushroom",
    "Garlic Chicken",
]

fake = Faker()
with app.app_context():
    print("Deleting entries 🚮🚮")
    Pizza.query.delete()
    Restaurant.query.delete()
    RestaurantPizza.query.delete()

    pizzas = list()
    print("seeding pizzas 🍕🍕")
    for pizza in pizza_flavors:
        pizza = Pizza(
            name=pizza,
            ingredients=fake.sentence(nb_words=10)
        )
        pizzas.append(pizza)
    db.session.add_all(pizzas)
    db.session.commit()

    restaurants = list()
    print("Seeding restaurants 🍽🍽")
    for i in range(25):
        restaurant = Restaurant(
            name=fake.company(),
            address=fake.address(),
        )
        restaurants.append(restaurant)

    db.session.add_all(restaurants)
    db.session.commit()

    print("Seeding respiz 🏨🍕")
    respizs = list()
    for i in range(25):
        respiz = RestaurantPizza(
            price=ri(1, 30),
            pizza_id=rc(pizzas).id,
            restaurant_id=rc(restaurants).id
        )
        respizs.append(respiz)

    db.session.add_all(respizs)
    db.session.commit()