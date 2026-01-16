


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

x = [559.3645487034573, 586.0538910128545, 595.5858059064716, 598.7631108710106, 565.0837073359928, 557.4581463320035]
y = [208.9819800006814, 217.88665705231062, 205.8017329972368, 186.72025097656962, 176.5434460075316, 191.80864132940903]






points_lists = get_points(x, y)
for l in points_lists:
    print(l)













