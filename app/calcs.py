

def get_points_list(all_x, all_y):
    points_list = []
    for index in range(len(all_x)):
        x = all_x[index]
        y = all_y[index]
        point = (int(round(x)), int(round(y)))
        points_list.append(point)
    return(points_list)

def get_multiple_points_lists(all_x, all_y):
    points_lists = []
    points = []
    for index in range(len(all_x)):
        if index in [100]: #[5, 5+6, 5+6+8, 5+6+8+4, 5+6+8+4+4, 5+6+8+4+4+4]:
            points_lists.append(points)
            points = []
        x = all_x[index]
        y = all_y[index]
        point = (int(round(x)), int(round(y)))
        points.append(point)
    points_lists.append(points)
    return(points_lists)

def round_mod(n, mult):
    return(mult * round(n/mult))

def round_and_square_pair(pair_of_points):
    p1 = pair_of_points[0]
    p3 = pair_of_points[1]
    x1, y1 = round_mod(p1[0], 5), round_mod(p1[1], 5)
    x2, y2 = round_mod(p3[0], 5), round_mod(p3[1], 5)
    
    p1 = (x1, y1)
    p2 = (x2, y1)
    p3 = (x2, y2)
    p4 = (x1, y2)

    return([p1, p2, p3, p4])

def make_pairs(points_list): #Takes a list of 2k points, returns k lists of pairs of points
    pairs_list = []
    for index in range(0, len(points_list), 2):
        pairs_list.append([points_list[index], points_list[index + 1]])
    return(pairs_list)

def get_squares_lists_from_pairs_of_points(pairs_list): #Takes a list of 2k points and every 2 points makes a square. Returns k lists, each representing a square
    squares = []
    for pair in pairs_list:
        squares.append(round_and_square_pair(pair))
    return(squares)

def make_squares_directly_from_points_list(all_x, all_y):
    points_list = get_points_list(all_x, all_y)
    pairs_list = make_pairs(points_list)
    squares = get_squares_lists_from_pairs_of_points(pairs_list)
    return(squares)

def make_precise_square(xy, xylen):
    (x1, y1), (xlen, ylen) = xy, xylen
    p1 = (x1, y1)
    p2 = (x1 + xlen, y1)
    p3 = (x1 + xlen, y1 + ylen)
    p4 = (x1, y1 + ylen)
    return([p1, p2, p3, p4])






x = [539.235138505854, 538.2661773260346, 552.8008168043241, 580.9010902248841, 621.5980807640949, 649.6983985408544, 661.3261101234862, 658.4191822278282, 677.7987163176141, 703.9610673785353, 741.7511300220881, 767.9134810830092, 779.5411926656408, 778.5721871296219, 765.0065531873513, 740.782124486069, 701.0541394828773, 665.2019991989634, 654.5432931523509, 654.5432931523509, 648.729437361035, 626.4429753755912, 587.683951552219, 555.7077446999821, 555.7077446999821]
y = [122.5752152024123, 110.15044069914508, 96.76990673874656, 88.16813725085797, 88.16813725085797, 96.76990673874656, 112.06194867569215, 128.30972819433802, 119.70795870644943, 114.92920517165501, 115.8849646287863, 124.4867341166749, 137.8672571393579, 149.33628312320934, 164.62832506015494, 171.31857563378094, 172.27433509091222, 159.8495496499295, 147.42478608437779, 137.8672571393579, 134.04424118626375, 141.69027309245206, 144.55752958841492, 136.9114976822266, 136.9114976822266]







#print(make_precise_square((1125, 16), (255, 155)))

#squares = make_squares_directly_from_points_list(x, y)
#for square in squares:
#    print(square)


print(get_points_list(x, y))











