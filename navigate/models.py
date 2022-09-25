from navigate import db
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Boolean, ForeignKey


class Customer(db.Model):
    customer_id = Column(Integer,primary_key=True)
    customer_name = Column(String(50))
    customer_coord = Column(String(8))
    customer_lat = Column(Float)
    customer_lng = Column(Float)

    def __repr__(self):
        return f'Customer: {self.customer_name}'


class Rider(db.Model):
    rider_id = Column(String(50),primary_key=True)
    name = Column(String(50))
    status = Column(Boolean, default=False)
    rider_coord = Column(String(50))
    rider_lat = Column(Float)
    rider_lng = Column(Float)
    rider_free_at = Column(TIMESTAMP)

    def __repr__(self):
        return f'Rider: {self.name}'

class Restaurant(db.Model):
    restaurant_id = Column(Integer,primary_key=True)
    restaurant_name = Column(String(50))
    restaurant_coord = Column(String(8))
    restaurant_lat = Column(Float)
    restaurant_lng = Column(Float)

    def __repr__(self):
        return f'Restaurant name: {self.restaurant_name}'



class Order(db.Model):
    id = Column(Integer, primary_key=True,autoincrement=True)
    order_id = Column(String(256))
    ordered_at = Column(TIMESTAMP)
    order_value = Column(Float)
    restaurant_id = Column(Integer)
    customer_id = Column(Integer)
    status = Column(Boolean, default=False)

    def __repr__(self):
        return f'Order value: {self.order_value}'

class History(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(256))
    order_pickup_time = Column(TIMESTAMP)
    order_delivery_time = Column(TIMESTAMP)
    order_delivery_distance = Column(Integer)
    rider_name = Column(String(50))
    restaurant_id=Column(Integer, ForeignKey("customer.customer_id"))
    customer_id=Column(Integer, ForeignKey("customer.customer_id"))
    directions_to_customer = Column(String(256))

    def __repr__(self):
        return f'Order pickup TIMESTAMP: {self.order_pickup_time}'

