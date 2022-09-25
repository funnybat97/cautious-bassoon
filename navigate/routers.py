from flask import render_template, request, jsonify
from navigate import db
from navigate import models
from navigate import app
from sqlalchemy import func, sql
from hashlib import sha256
from navigate import culc_path


@app.route('/', methods=['GET'])
def index():
    history = db.session \
        .query(models.History)\
        .order_by(models.History.order_id.desc())\
        .all()
    return render_template('index.html', history=history)


@app.route('/api/', methods=['GET'])
def index_api():
    history = db.session \
        .query(models.History) \
        .order_by(models.History.order_id.desc()) \
        .all()
    res = []
    for order in history:
        res.append({
            'id': order.id,
            'order_id': order.order_id,
            'order_pickup_time': order.order_pickup_time,
            'order_delivery_time': order.order_delivery_time,
            'order_delivery_distance': order.order_delivery_distance,
            'rider_name': order.rider_name,
            'restaurant_id': order.restaurant_id,
            'customer_id': order.customer_id,
            'directions_to_customer': order.directions_to_customer,
        })

    return jsonify(res)


@app.route('/api/farthest_rider')
def get_farthest_rider():
    res = db.session \
        .query(models.History.rider_name, func.sum(models.History.order_delivery_distance)) \
        .group_by(models.History.rider_name) \
        .order_by(sql.text("2")).first()

    return {
        "rider_name": res[0],
        "distance": res[1]
    }


@app.route('/api/busiest_restaurant')
def get_busiest_restaurant():
    res = db.session \
        .query(models.History.restaurant_id, func.count(models.History.id)) \
        .group_by(models.History.restaurant_id) \
        .order_by(sql.text("2")).first()

    restaurant = models.Restaurant.query.filter_by(restaurant_id=res[0]).first()

    return {
        "restaurant_name": restaurant.restaurant_name,
        "count": res[1]
    }


@app.route('/api/biggest_appetite')
def get_biggest_appetite():
    res = db.session \
        .query(models.Order.customer_id, func.sum(models.Order.order_value)) \
        .group_by(models.Order.customer_id) \
        .order_by(sql.text("2")).first()

    customert = models.Customer.query.filter_by(customer_id=res[0]).first()

    return {
        "customer_name": customert.customer_name,
        "value": res[1]
    }
@app.route('/api/add_new_order', methods=['POST'])
def add_new_customer():
    data = request.get_json()
    username_hash = sha256(
        (
                str(data['ordered_at']) +
                str(data['customer_id']) +
                str(data['restaurant_id']) +
                str(data['order_value'])
        ).encode('utf-8')
    ).hexdigest()

    new_order = models.Order(
        order_id=username_hash,
        ordered_at=data['ordered_at'],
        order_value=data['order_value'],
        restaurant_id=data['restaurant_id'],
        customer_id=data['customer_id']
    )
    db.session.add(new_order)
    new_order = models.Order.query.filter_by(order_id=username_hash).first()
    culc_path.pick_order(new_order)
    history = models.History.query.filter_by(order_id=username_hash).first()
    return {
        'id': history.id,
        'order_id': history.order_id,
        'order_pickup_time': history.order_pickup_time,
        'order_delivery_time': history.order_delivery_time,
        'order_delivery_distance': history.order_delivery_distance,
        'rider_name': history.rider_name,
        'restaurant_id': history.restaurant_id,
        'customer_id': history.customer_id,
        'directions_to_customer': history.directions_to_customer,
    }
