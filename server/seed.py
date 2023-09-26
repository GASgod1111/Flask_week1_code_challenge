from faker import Faker
from my_app import app, my_db, MyPizza, MyRestaurantPizza, MyRestaurant

fake = Faker()

def generate_custom_pizza():
    return {
        'pizza_name': fake.word(),
        'pizza_ingredients': ', '.join(fake.words(nb=5)),
    }

def generate_custom_restaurant():
    return {
        'restaurant_name': fake.company(),
        'restaurant_address': fake.address(),
    }

def seed_custom_database():
    with app.app_context():
        custom_pizzas = []
        custom_restaurants = []

        for _ in range(50): 
            pizza_data = generate_custom_pizza()
            custom_pizza = MyPizza(**pizza_data)
            custom_pizzas.append(custom_pizza)
            my_db.session.add(custom_pizza)

        for _ in range(20): 
            restaurant_data = generate_custom_restaurant()
            custom_restaurant = MyRestaurant(**restaurant_data)
            custom_restaurants.append(custom_restaurant)
            my_db.session.add(custom_restaurant)

        for custom_pizza in custom_pizzas:
            for custom_restaurant in custom_restaurants:
                price = fake.random_int(min=1, max=30)
                custom_restaurant_pizza = MyRestaurantPizza(restaurant=custom_restaurant, pizza=custom_pizza, pizza_price=price)
                my_db.session.add(custom_restaurant_pizza)

        my_db.session.commit()

if __name__ == '__main__':
    seed_custom_database()
