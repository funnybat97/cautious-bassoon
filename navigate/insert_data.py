import json
from navigate import db
from navigate import app
from sqlalchemy import create_engine, MetaData

from navigate import models
from navigate import culc_path
import pathlib

path = str(pathlib.Path(pathlib.Path(__file__).parent.resolve()).parent.resolve())
# Read data from CSV and load into a dataframe object
restaurants_path = path + '/data/restaurants.json'
orders_path = path + '/data/orders.json'
customers_path = path + '/data/customers.json'
riders_path = path + '/data/riders.json'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


def drop_tables():
    metadata = MetaData()
    metadata.reflect(bind=engine)

    table = metadata.tables.get('history')
    if table is not None:
        models.History.__table__.drop(engine)

    table = metadata.tables.get('order')
    if table is not None:
        models.Order.__table__.drop(engine)

    table = metadata.tables.get('customer')
    if table is not None:
        models.Customer.__table__.drop(engine)

    table = metadata.tables.get('rider')
    if table is not None:
        models.Rider.__table__.drop(engine)

    table = metadata.tables.get('restaurant')
    if table is not None:
        models.Restaurant.__table__.drop(engine)


def insert_default_data():
    db.create_all()
    with open(customers_path) as my_file:
        models.Customer.query.delete()
        data = json.load(my_file)
        for item in data:
            new_customer = models.Customer(
                customer_id=item['customer_id'],
                customer_name=item['customer_name'],
                customer_coord=item['customer_coord'],
                customer_lat=item['customer_lat'],
                customer_lng=item['customer_lng']
            )
            db.session.add(new_customer)

    with open(restaurants_path) as my_file:
        models.Restaurant.query.delete()
        data = json.load(my_file)
        for item in data:
            new_restaurant = models.Restaurant(
                restaurant_id=item['restaurant_id'],
                restaurant_name=item['restaurant_name'],
                restaurant_coord=item['restaurant_coord'],
                restaurant_lat=item['restaurant_lat'],
                restaurant_lng=item['restaurant_lng']
            )
            db.session.add(new_restaurant)

    with open(riders_path) as my_file:
        models.Rider.query.delete()
        data = json.load(my_file)
        for item in data:
            new_rider = models.Rider(
                rider_id=item['rider_id'],
                name=item['name']
            )
            db.session.add(new_rider)

    with open(orders_path) as my_file:
        models.Order.query.delete()
        data = json.load(my_file)
        for item in data:
            new_customer = models.Order(
                order_id=item['order_id'],
                ordered_at=str(item['ordered_at']),
                order_value=item['order_value'],
                restaurant_id=item['restaurant_id'],
                customer_id=item['customer_id']
            )
            db.session.add(new_customer)

    db.session.commit()


def cal_order_history():
    orders = models.Order.query.all()
    for order in orders:
        culc_path.pick_order(order)


