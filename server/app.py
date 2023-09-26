from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from my_models import MyPizza, MyRestaurantPizza, MyRestaurant, db
from flask_restful import Api, Resource

# Create a Flask application instance
app = Flask(__name__)

# Configure database URI and disable track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_pizza_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration objects
migrate = Migrate(app, db)

# db = SQLAlchemy(app)
db.init_app(app)

api = Api(app)

class MyPizzas(Resource):

    def get(self):
        pizzas = []

        all_pizzas = MyPizza.query.all()

        for pizza in all_pizzas:
            pizzas.append(pizza.to_dict()) 

        response = make_response(
            jsonify(pizzas),
            200
        )

        return response

api.add_resource(MyPizzas, '/pizzas')

class MyRestaurants(Resource):

    def get(self):
        restaurants = []
        all_restaurants = MyRestaurant.query.all()

        for restaurant in all_restaurants:
            restaurants.append(restaurant.to_dict())
        
        response  = make_response(
            jsonify(restaurants),
            200
        )

        return response

api.add_resource(MyRestaurants, '/restaurants')

class MyRestaurantById(Resource):

    def get(self, id):
        restaurant = MyRestaurant.query.filter_by(id=id).first()

        if restaurant is None:
            response_dict = {"error": "Restaurant not found"}
            response = make_response(
                jsonify(response_dict),
                404
            )
            return response

        pizzas = MyRestaurantPizza.query.filter_by(restaurant_id=restaurant.id).all()

        pizzas_dict = [pizza.to_dict() for pizza in pizzas]

        response_dict = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": pizzas_dict
        }

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
    
    def delete(self, id):
        restaurant = MyRestaurant.query.filter_by(id=id).first()

        if restaurant is None:
            response_dict = {"error": "Restaurant not found"}
            response = make_response(
                jsonify(response_dict),
                404
            )
            return response

        db.session.delete(restaurant)
        db.session.commit()

        response_dict = {"message": "Restaurant deleted successfully"}
        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

api.add_resource(MyRestaurantById, '/restaurant/<int:id>')

class MyRestaurantPizzas(Resource):

    def post(self):
        new_restaurant_pizza = MyRestaurantPizza(
            price=request.json['price'],
            pizza_id=request.json['pizza_id'],
            restaurant_id=request.json['restaurant_id']
        )

        if not new_restaurant_pizza.is_valid():
            response_dict = {"errors": ["validation errors"]}
            response = make_response(
                jsonify(response_dict),
                400
            )
            return response

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        pizza = MyPizza.query.get(new_restaurant_pizza.pizza_id)

        response_dict = {
            "id": new_restaurant_pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }

        response = make_response(
            jsonify(response_dict),
            201
        )

        return response

api.add_resource(MyRestaurantPizzas, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
