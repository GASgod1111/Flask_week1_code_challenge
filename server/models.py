from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from flask import Flask

# Create a SQLAlchemy instance
my_db = SQLAlchemy()

# Create Pizza model
class MyPizza(my_db.Model):
    __tablename__ = 'my_pizzas'

    pizza_id = my_db.Column(my_db.Integer, primary_key=True)
    pizza_name = my_db.Column(my_db.String)
    pizza_ingredients = my_db.Column(my_db.String)
    created_at = my_db.Column(my_db.DateTime, default=datetime.utcnow)
    updated_at = my_db.Column(my_db.DateTime, default=datetime.utcnow)
    
    # Add relationship to RestaurantPizza class
    pizza_restaurant_relationship = my_db.relationship('MyRestaurantPizza', back_populates='pizza')

    def to_dict(self):
        return {
            "id": self.pizza_id,
            "name": self.pizza_name,
            "ingredients": self.pizza_ingredients,
        }

# Create RestaurantPizza model
class MyRestaurantPizza(my_db.Model):
    __tablename__ = 'my_restaurant_pizzas'

    pizza_relationship_id = my_db.Column(my_db.Integer, primary_key=True)
    pizza_id = my_db.Column(my_db.Integer, my_db.ForeignKey('my_pizzas.pizza_id'))
    restaurant_id = my_db.Column(my_db.Integer, my_db.ForeignKey('my_restaurants.restaurant_id'))
    pizza_price = my_db.Column(my_db.Integer, CheckConstraint('pizza_price >= 1 AND pizza_price <= 30'), nullable=False) 
    created_at = my_db.Column(my_db.DateTime, default=datetime.utcnow)
    updated_at = my_db.Column(my_db.DateTime, default=datetime.utcnow)
    
    # Add relationships to Restaurant and Pizza
    restaurant = my_db.relationship('MyRestaurant', back_populates='restaurant_pizzas')
    pizza = my_db.relationship('MyPizza', back_populates='pizza_restaurant_relationship')

    def to_dict(self):
        return {
            "price": self.pizza_price,
            "pizza_id": self.pizza_id,
            "restaurant_id": self.restaurant_id,
        }

    def is_valid(self):
        if self.pizza_price < 0:
            return False
        return True

# Create Restaurant model
class MyRestaurant(my_db.Model):
    __tablename__ = 'my_restaurants'

    restaurant_id = my_db.Column(my_db.Integer, primary_key=True)
    restaurant_name = my_db.Column(my_db.String(50), unique=True, nullable=False)
    restaurant_address = my_db.Column(my_db.String)
    
    # Define a relationship to RestaurantPizza
    restaurant_pizzas = my_db.relationship('MyRestaurantPizza', back_populates='restaurant')

    def to_dict(self):
        return {
            "id": self.restaurant_id,
            "name": self.restaurant_name,
            "address": self.restaurant_address
        }
