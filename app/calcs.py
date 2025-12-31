


def get_points(all_x, all_y):
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

x = [4072.7471992818087, 4072.7471992818087, 422.13707296998024, 459.4571125656384]
y = [779.1593476238974, -0.9725738216258792, 15.075576066468887, 808.7049765458637]






points_lists = get_points(x, y)
for l in points_lists:
    print(l)













