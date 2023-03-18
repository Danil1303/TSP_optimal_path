class Point:
    __slots__ = ['point_x', 'point_y']
    points_dict = {}
    point_number = 1

    def __init__(self, x, y):
        self.point_x = x
        self.point_y = y
        self.points_dict[Point.point_number] = self
        Point.point_number += 1

    @classmethod
    def delete_points(cls):
        cls.points_dict = {}
        cls.point_number = 1


class Ant:
    __slots__ = ['route']
    ants_list = []

    def __init__(self):
        self.route = [1]
        Ant.ants_list.append(self)

    @classmethod
    def delete_ants(cls):
        cls.ants_list = []
