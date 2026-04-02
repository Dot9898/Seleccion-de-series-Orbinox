

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





x = [2020.111732670964, 1939.3694240454045, 1855.5214506454731, 1756.14633801847, 1656.7711069269883, 1541.8684996794775, 1405.2275421206302, 1302.746883183734, 1163.0004977794727, 1066.730812997884, 989.0939322177386, 914.5624792830076, 840.0310263482766, 793.4488978801894, 759.2887177227169]
y = [489.98153320312497, 530.4404808872767, 567.7872474888393, 595.7972927594866, 623.8073380301339, 642.4807213309151, 661.1540452706473, 667.3786448800223, 664.2662857142857, 658.041864188058, 642.4807213309151, 623.8073380301339, 589.572930594308, 558.4506448800223, 517.9915784737723]




#[(2020, 490), (1939, 530), (1856, 568), (1756, 596), (1657, 624), (1542, 642), (1405, 661), (1303, 667), (1163, 664), (1067, 658), (989, 642), (915, 624), (840, 590), (793, 558), (759, 518)]
#'Relaves': [(3455, 531), (3425, 618), (3231, 687), (3003, 680), (2843, 610), (2828, 568), (2714, 560), (2560, 620), (2323, 625), (2181, 580), (2137, 506), (2005, 503), (1673, 633), (1275, 673), (959, 650), (797, 577), (752, 494), (780, 391), (1028, 245), (1402, 145), (1854, 145), (2051, 204), (2124, 249), (2155, 335), (2124, 401), (2214, 411), (2331, 380), (2504, 366), (2684, 401), (2749, 463), (2860, 473), (3025, 426), (3195, 426), (3359, 459)]}
#[(2017, 493), (1936, 534), (1834, 577), (1716, 611), (1626, 636), (1529, 655), (1433, 670), (1371, 677), (1191, 677), (1079, 674), (980, 658), (880, 630), (800, 577), (753, 524), (750, 459), (784, 406), (871, 328), (936, 297), (1017, 263), (1088, 235), (1185, 207), (1272, 182), (1377, 163), (1489, 148), (1626, 148), (1769, 145), (1871, 157), (1961, 176), (2045, 207), (2110, 238), (2147, 291), (2151, 347), (2129, 384), (2113, 409), (2206, 412), (2287, 390), (2368, 378), (2452, 378), (2542, 381), (2601, 387), (2666, 406), (2716, 428), (2731, 443), (2747, 468), (2859, 471), (2908, 450), (2964, 437), (3048, 425), (3141, 425), (3210, 428), (3281, 440), (3355, 459), (3414, 490), (3449, 534), (3446, 583), (3427, 611), (3393, 642), (3318, 667), (3237, 683), (3147, 686), (3067, 680), (2983, 667), (2902, 646), (2843, 605), (2824, 565), (2719, 558), (2678, 593), (2616, 608), (2542, 621), (2461, 627), (2383, 627), (2312, 624), (2250, 608), (2200, 580), (2157, 546), (2144, 527), (2141, 499)]


#print(make_precise_square((1125, 16), (255, 155)))

#squares = make_squares_directly_from_points_list(x, y)
#for square in squares:
#    print(square)


print(get_points_list(x, y))











