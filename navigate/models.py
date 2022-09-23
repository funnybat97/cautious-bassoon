from navigate import db
from sqlalchemy import Column, Integer, String, Sequence, Float, Time, Boolean, ForeignKey


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
    order_id = Column(String(50), primary_key=True)
    ordered_at = Column(Time)
    order_value = Column(Float)
    restaurant_id = Column(Integer)
    customer_id = Column(Integer)
    status = Column(Boolean)

    def __repr__(self):
        return f'Order value: {self.order_value}'

class History(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(50), ForeignKey("order.order_id"))
    order_pickup_time = Column(Time)
    order_pickup_time = Column(Time)
    order_delivery_distance = Column(Integer)
    rider_name = Column(String(50))
    restaurant_id=Column(Integer, ForeignKey("customer.customer_id"))
    customer_id=Column(Integer, ForeignKey("customer.customer_id"))
    directions_to_customer = Column(String(256))

    def __repr__(self):
        return f'Order pickup time: {self.order_pickup_time}'

