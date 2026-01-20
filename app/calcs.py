


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

x = [639.7743300423131, 567.8984485190409, 481.80535966149506, 488.9139633286319, 558.4203102961918]
y = [93.12745098039215, 288.85294117647055, 280.171568627451, 133.37745098039215, 83.65686274509804]








points_lists = get_points(x, y)
for l in points_lists:
    print(l)













