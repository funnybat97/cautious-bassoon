import geopy.distance

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
    print(path)
    return path

# get distance between two points
def get_rider_distance(x1, y1, x2, y2):
    return geopy.distance.geodesic((x1,y1), (x2,y2)).m

# Driver code
if __name__ == '__main__':
    src = coord_converter('D7')
    dest = coord_converter('F3')
    get_path(src, dest)

