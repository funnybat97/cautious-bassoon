import pandas
from navigate import db
from navigate import app
from sqlalchemy import create_engine, MetaData, cast, Date, func
import json
from navigate import models
from navigate import culc_path
import pathlib
import datetime

print(str(pathlib.Path(__file__).parent.resolve()) + '/restaurants.json')
path = str(pathlib.Path(__file__).parent.resolve())
# Read data from CSV and load into a dataframe object
restaurants_path = path + '/restaurants.json'
orders_path = path + '/orders.json'
customers_path = path + '/customers.json'
riders_path = path + '/riders.json'
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
    print(orders)
    for order in orders:
        order_restaurant = models.Restaurant.query.filter_by(restaurant_id=order.restaurant_id).first()
        order_customer = models.Customer.query.filter_by(customer_id=order.customer_id).first()
        rider = models.Rider.query.filter_by(status=False).first()

        if rider:
            src = culc_path.coord_converter(order_restaurant.restaurant_coord)
            dest = culc_path.coord_converter('F3')
            distance_to_restaurant = 0
            distance_to_customer = culc_path.get_rider_distance(
                order_restaurant.restaurant_lng,
                order_restaurant.restaurant_lat,
                order_customer.customer_lng,
                order_customer.customer_lat
            )
            distance = distance_to_restaurant + distance_to_customer
            path_to_restaurant = culc_path.get_path(
                culc_path.coord_converter('', True),
                culc_path.coord_converter(order_restaurant.restaurant_coord)
            )
            path_to_customer = culc_path.get_path(
                culc_path.coord_converter(order_restaurant.restaurant_coord),
                culc_path.coord_converter(order_customer.customer_coord)
            )
            full_path = path_to_restaurant + path_to_customer
            order_delivery_time = order.ordered_at+datetime.timedelta(minutes=round(distance / 100))
            history = models.History(
                order_id=order.order_id,
                order_pickup_time=order.ordered_at,
                order_delivery_time=order_delivery_time,
                order_delivery_distance=distance,
                rider_name=rider.name,
                restaurant_id=order.restaurant_id,
                customer_id=order.customer_id,
                directions_to_customer=full_path
            )
            print(rider)
            rider.status = True
            rider.rider_coord = order_customer.customer_coord
            rider.rider_lat = order_customer.customer_lat
            rider.rider_lng = order_customer.customer_lng
            db.session.add(history)
            db.session.commit()
        else:
            # print('no rider')
            # sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            # print(order_restaurant.restaurant_lng)
            # print(order_restaurant.restaurant_lat)
            # result = db.engine.execute(f'''
            # select min(sqrt(
            # power({order_restaurant.restaurant_lng}-rider_lng,2)
            # +
            # power({order_restaurant.restaurant_lat}-rider_lat,2)
            # ))
            #   from rider
            # ''').first()
            # rider = db.session.query(models.Rider).values(func.min(
            #     culc_path.get_rider_distance(
            #         models.Rider.rider_lng,
            #         models.Rider.rider_lat,
            #         order_restaurant.restaurant_lng,
            #         order_restaurant.restaurant_lat,
            #     )
            #     +
            #     culc_path.get_rider_distance(
            #         order_restaurant.restaurant_lng,
            #         order_restaurant.restaurant_lat,
            #         order_customer.customer_lng,
            #         order_customer.customer_lat
            #     )
            #
            # ))
            # print(result)

            pass
    pass


if __name__ == '__main__':
    drop_tables()
    insert_default_data()
    cal_order_history()
    # app.run(port=5000)
