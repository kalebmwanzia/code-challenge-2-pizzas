from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource

from models import Restaurant, RestaurantPizza, Pizza, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):
    def get(self):
        return {}, 200


class Restaurants(Resource):
    def get(self):
        restaurants = [restaurant.to_dict()
                       for restaurant in Restaurant.query.all()]
        response = make_response(jsonify(restaurants), 200)
        return response


class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            return {"error": "404 restaurant not found"}, 404

        response = make_response(jsonify(restaurant.to_dict()), 200)
        return response

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            return {"error": "404 restaurant not found"}, 404

        db.session.delete(restaurant)
        db.session.commit()

        return {}, 200


class Pizzas(Resource):
    def get(self):
        pizzas = [pizza.to_dict()
                  for pizza in Pizza.query.all()]
        response = make_response(jsonify(pizzas), 200)
        return response


class RestaurantPizzas(Resource):
    def post(self):
        try:
            data = request.get_json()
            respiz = RestaurantPizza(**data)
            db.session.add(respiz)
            db.session.commit()
            return respiz.to_dict(), 201
        except ValueError as err:
            return {"errors": str(err)}, 401


api.add_resource(Home, '/', endpoint='/')
api.add_resource(Restaurants, '/restaurants', endpoint='restaurants')
api.add_resource(RestaurantById, '/restaurants/<int:id>', endpoint='<int:id>')
api.add_resource(Pizzas, '/pizzas', endpoint='pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas',
                 endpoint="restaurant_pizzas")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
