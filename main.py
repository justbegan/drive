
from route_api_imetate import ImitateGeoApi
from open_route import get_route as open_route

REAL_API_MODE = True


def get_rounded_coords(coords: list, girth: int) -> list:
    result = []
    for i in coords:
        result.append([round(i[0], girth), round(i[1], girth)])
    return result


def get_dirrection(coords: list) -> int:
    lat1, lon1 = coords[0]
    lat2, lon2 = coords[1]
    x = lat1 - lat2
    y = lon1 - lon2
    if x > 0 and y > 0:
        return 0
    elif x > 0 and y < 0:
        return 1
    elif x < 0 and y > 0:
        return 2
    else:
        return 3


def calculate_priority(num: int, coords: list, girth: int) -> dict:
    """Вычисляет приоритет заказа
    Args:
        num (int): id заказа
        coords (list): координаты заказа
        girth (int): радиус обхвата чем меньше чем выше приоритет

    Returns:
        dict: объект
    """
    lat1, lon1 = coords[0]
    lat2, lon2 = coords[1]
    x = abs(lat1 - lat2) * girth
    y = abs(lon1 - lon2) * girth
    return {
        "id": num,
        "priority": round(x if x > y else y, 2),
        "coords": coords
    }


def main(driver_coord: list, orders_coord: list) -> list:
    """Функция выбирает подходящие маршруты

    Args:
        order_coords (list): список заказов
        driver_route (list): координаты водителя

    Returns:
        list: подходящие заказы
    """
    if REAL_API_MODE:  # постройка маршрута через сервис api.openrouteservice.org
        driver_route = open_route(*driver_coord)
    else:
        api = ImitateGeoApi()  # имитация маршрута через рандом
        driver_route = api.get_route_coords(driver_coord)

    result = []
    driver_dirrection = get_dirrection(driver_coord)

    for girth in range(2, 0, -1):
        driver_roundet_coords = get_rounded_coords(driver_route, girth)
        for num, p_coords in enumerate(orders_coord, start=1):
            if p_coords is not None:
                passager_dirrection = get_dirrection(p_coords)
                if all([
                    get_rounded_coords(p_coords, girth)[0] in driver_roundet_coords,  # проверка начальных координат
                    get_rounded_coords(p_coords, girth)[1] in driver_roundet_coords,  # проверка конечных координат
                    driver_dirrection == passager_dirrection
                ]):
                    result.append(calculate_priority(num, p_coords, girth))
                    orders_coord[num - 1] = None
    return result


if __name__ == "__main__":

    point_1 = [129.73858455981434, 62.04893351502969]
    point_2 = [128.05160515520697, 62.14991308479122]
    driver_coord = [point_1, point_2]

    order_1 = [point_1, point_2]
    order_2 = [[129.61776499889748, 62.04759688568939], [129.54337717749496, 62.065645910911684]]
    order_3 = [[129.76418500413843, 62.05186918060241], [129.90752620676398, 61.970360340311885]]
    order_4 = [[129.64138819140987, 62.04325738220368], [129.57656259866525, 62.0521995418888]]

    orders = [
        order_1,
        order_2,
        order_3,
        order_4
    ]
    print(main(driver_coord, orders))
