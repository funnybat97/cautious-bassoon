import geopy.distance
from navigate import db
from navigate import models
from navigate import culc_path
import datetime

# maping filed to numbers
y_fields = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7,
    'H': 8,
    'I': 9,
    'J': 10,
    'K': 11,
}
# grid size
grid = {
    "x": 8,
    "y": 11
}


# converting coords function
def coord_converter(coord, default=False):
    if default:
        return {
            "x": 4,
            "y": 3
        }
    else:
        return {
            "x": int(coord[1]),
            "y": y_fields[coord[0]],
        }
    pass


# validation cell if its out of grid
def isValid(x, y):
    if x >= 1 and x <= grid['x'] and y >= 1 and y <= grid['y']:
        return True
    return False


# calculate distance between two cells
def calculate_distance(x, y, dx, dy):
    return abs(dx - x) + abs(dy - y)


# get distance between two cells
def get_distance(x, y, dx, dy):
    if isValid(x, y):
        return calculate_distance(x, y, dx, dy)
    else:
        return max([grid['x'], grid['y']])


# define next step coords
def get_next_step(x, y, dx, dy, sum):
    # distance if moves north
    sum_n = get_distance(x - 1, y, dx, dy)

    # distance if moves south
    sum_s = get_distance(x + 1, y, dx, dy)

    # distance if moves west
    sum_w = get_distance(x, y - 1, dx, dy)

    # distance if moves east
    sum_e = get_distance(x, y + 1, dx, dy)

    moves_names = ['N', 'S', 'W', 'E']
    moves = [sum_n, sum_s, sum_w, sum_e]
    sum = min(moves)
    next_move = moves_names[moves.index(sum)]

    if next_move == 'N':
        x = x - 1
    elif next_move == 'S':
        x = x + 1
    elif next_move == 'W':
        y = y - 1
    elif next_move == 'E':
        y = y + 1

    return sum, next_move, x, y


# get path between to cells
def get_path(source, destination):
    x = source['x']
    y = source['y']
    dx = destination['x']
    dy = destination['y']
    sum = get_distance(x, y, dx, dy)
    path = ''
    while sum != 0:
        sum, next_move, x, y = get_next_step(x, y, dx, dy, sum)
        path = path + next_move

    return path

# get distance between two points
def get_rider_distance(x1, y1, x2, y2):
    return geopy.distance.geodesic((x1,y1), (x2,y2)).m

# pick_next_rider_for_order
def pick_order(order):
    order_restaurant = models.Restaurant.query.filter_by(restaurant_id=order.restaurant_id).first()
    order_customer = models.Customer.query.filter_by(customer_id=order.customer_id).first()
    rider = models.Rider.query.filter_by(status=False).first()

    if rider:
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
        order_delivery_time = order.ordered_at + datetime.timedelta(minutes=round(distance / 100))
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

        rider.status = True
        rider.rider_coord = order_customer.customer_coord
        rider.rider_lat = order_customer.customer_lat
        rider.rider_lng = order_customer.customer_lng
        rider.rider_free_at = order_delivery_time
        db.session.add(history)
        db.session.commit()
    else:
        result = db.engine.execute(f'''
                select r.rider_id,
                   (ST_DistanceSphere(
                        ST_MakePoint({order_restaurant.restaurant_lng},{order_restaurant.restaurant_lat}),
                        ST_MakePoint(r.rider_lng,r.rider_lat )
                    )
                    +
                    ST_DistanceSphere(
                        ST_MakePoint(r.rider_lng,r.rider_lat),
                        ST_MakePoint({order_customer.customer_lng},{order_customer.customer_lat})
                    ))::int as order_delivery_distance,
                     r.rider_free_at + ((ST_DistanceSphere(
                        ST_MakePoint({order_restaurant.restaurant_lng},{order_restaurant.restaurant_lat}),
                        ST_MakePoint(r.rider_lng,r.rider_lat )
                    )
                    +
                    ST_DistanceSphere(
                        ST_MakePoint(r.rider_lng,r.rider_lat),
                        ST_MakePoint({order_customer.customer_lng},{order_customer.customer_lat})
                    )::int)/100 * interval '1 minute') as order_delivery_time
                from rider r
                order by 3
                ''').first()
        rider = models.Rider.query.filter_by(rider_id=result[0]).first()
        distance = result[1]
        path_to_restaurant = culc_path.get_path(
            culc_path.coord_converter(rider.rider_coord),
            culc_path.coord_converter(order_restaurant.restaurant_coord)
        )
        path_to_customer = culc_path.get_path(
            culc_path.coord_converter(order_restaurant.restaurant_coord),
            culc_path.coord_converter(order_customer.customer_coord)
        )
        full_path = path_to_restaurant + path_to_customer
        order_delivery_time = result[2]
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

        rider.status = True
        rider.rider_coord = order_customer.customer_coord
        rider.rider_lat = order_customer.customer_lat
        rider.rider_lng = order_customer.customer_lng
        rider.rider_free_at = order_delivery_time
        db.session.add(history)
        db.session.commit()


