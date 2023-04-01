class Point:
    __slots__ = ['point_x', 'point_y']
    points_dict = {}
    point_number = 1

    def __init__(self, x, y) -> None:
        self.point_x = x
        self.point_y = y
        self.points_dict[Point.point_number] = self
        Point.point_number += 1

    @classmethod
    def delete_points(cls) -> None:
        cls.points_dict = {}
        cls.point_number = 1


class Ant:
    __slots__ = ['route', 'total_distance']
    ants_list = []

    def __init__(self) -> None:
        self.route = [1]
        Ant.ants_list.append(self)
        self.total_distance = 0

    def clear_ant_info(self) -> None:
        self.route = [1]
        self.total_distance = 0

    @classmethod
    def delete_ants(cls) -> None:
        cls.ants_list = []
