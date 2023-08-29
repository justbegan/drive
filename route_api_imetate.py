import random


class ImitateGeoApi:
    """
    Имитация geo апи из линии создает псевдо повороты через рандом
    """

    POINTS_COUNTS = 100  # количество создоваемых точек
    RANDOM_SPREAD = 0.008  # разброс рандома

    def get_route_coords(self, coords: list) -> list:
        lat1, lon1 = coords[0]
        lat2, lon2 = coords[1]

        return [
            [
                self.calculate_new_point(lat1, lat2, num),
                self.calculate_new_point(lon1, lon2, num)
            ] for num in range(self.POINTS_COUNTS + 1)
        ]

    def calculate_new_point(self, coord1, coord2, num):
        fraction = num / self.POINTS_COUNTS
        return coord1 + fraction * (coord2 - coord1) + self.get_random(num)

    def get_random(self, num: int) -> int:
        if num == 0 or num == self.POINTS_COUNTS:
            return 0
        return random.uniform(-1 * (self.RANDOM_SPREAD), self.RANDOM_SPREAD)
