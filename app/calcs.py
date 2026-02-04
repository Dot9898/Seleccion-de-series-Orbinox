

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




x = [5.840281767980034, 4.866901473316695, 229.71861842123127, 229.71861842123127]
y = [4.850769260726268, 130.97014552528768, 132.91045322957814, 3.880607081723365]





#squares = make_squares_directly_from_points_list(x, y)
#for square in squares:
#    print(square)

print(get_points_list(x, y))











