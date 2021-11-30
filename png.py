from functools import reduce
from cairo import SVGSurface, Context, Matrix, LINE_CAP_ROUND
from config import config


def do_circle(obj: Context, x: int, y: int) -> None:
    """ do circle in obj, this cairo
        x - коррдината по х
        y - коррдината по у
        """
    y = config['HEIGHT'] - y

    obj.save()
    obj.set_line_width(6.0)
    obj.arc(x, y, 10, 0, 2 * 3.14)
    obj.stroke_preserve()
    obj.set_source_rgb(0, 0.2, 0.8)
    obj.fill()
    obj.restore()


def do_cairo():
    """ Создаёт полотно для рисование объектов """
    svg = SVGSurface(config['NAME_SVG'], config['WIDTH'], config["HEIGHT"])
    holst = Context(svg)
    m = Matrix(yy=-1, y0=config['HEIGHT'])
    holst.transform(m)
    holst.save()
    holst.set_source_rgb(0.3, 0.3, 0.05)
    holst.paint()
    holst.restore()
    return holst, svg


def save_cairo(svg: SVGSurface, filename: str = config["NAME_PNG"]) -> None:
    """ Сохраняет в пнг и свг форматах """
    if config['save_or_not_png']:
        svg.write_to_png(filename)
    svg.finish()


def graham_convex_hull(points):
    """
    Алгоритм Грэтхема, который работает со сложность n log2(n)
    """
    turn_left, turn_right, turn_none = (1, -1, 0)

    def cmp(a, b):
        """ возвращает 1, 0 , -1 в зависимости от значений а и б.
        if a > b: 1
        if a == b: 0
        if a < b: -1
        """
        return (a > b) - (a < b)

    def turn(one, two, free):
        """
        Находит произведение векторов и передаёт их в cmp
        Это тоже самое, что если бы искал алгоритм: синус между угла,
        и если больше 180 градусов, который внутри оболочки
        https://prnt.sc/20y6cia
        cmp((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1), 0)
        Если синус < 180: 1
        Если синус = 180: 0
        Если синус > 180: -1
        """
        dx21 = two[0] - one[0]
        dy31 = free[1] - one[1]
        vector1 = dx21 * dy31
        dx31 = free[0] - one[0]
        dy21 = two[1] - one[1]
        vector2 = dx31 * dy21
        return cmp((vector1 - vector2), 0)

    def _keep_left(hull, r):
        """ При -1, точка не считается частью выпуклой оболочки и удаляется из списка(стэка) """
        while len(hull) > 1 and turn(hull[-2], hull[-1], r) != turn_left:
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull

    points = sorted(points)  # сортирует по х
    # reduce - через фор забирает все значения из поинт и запихивает их в _keep_left(value, [])
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])
    return l.extend(u[1:-1]) or l


def read_file() -> [int, int]:
    test_data = []
    with open(config['FILE_NAME'], 'r') as f:
        f.readline()
        for i in f:
            x, y = map(int, i.split())
            test_data.append([x, y])
    return test_data


def draw_line(obj: Context, x1: int, y1: int, x2: int, y2: int, color: int = 0, width: int = 5) -> None:
    y1 = config["HEIGHT"] - y1
    y2 = config["HEIGHT"] - y2
    obj.set_line_cap(LINE_CAP_ROUND)
    if not color:
        color = [1, 1, 1, 1]
    else:
        if not isinstance(color, int):
            raise "color isn't type int"
        _c = list()
        for i in str(color):
            _c.append(int(i))
        color = _c
    obj.set_source_rgba(*color)
    obj.set_line_width(width)
    obj.move_to(x1, y1)
    obj.line_to(x2, y2)
    obj.stroke_preserve()


def do_line(holst, points):
    for i, v in enumerate(points):
        if points[i] == points[-1]:
            draw_line(holst, *points[0], *points[-1])
            break
        draw_line(holst, *v, *points[i + 1])


def main():
    holst, svg = do_cairo()
    test_data = read_file()
    # start_time = time.time()
    result = graham_convex_hull(test_data)
    # print((time.time() - start_time))
    for i in test_data:
        do_circle(holst, *i)
    do_line(holst, result)
    save_cairo(svg)


if __name__ == '__main__':
    main()
