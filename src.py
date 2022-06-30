from functools import reduce
from cairo import SVGSurface, Context, Matrix, LINE_CAP_ROUND
import config as cfg


def draw_circle(obj: Context, x: int, y: int) -> None:
    """ draw circle in obj, this cairo """
    y = cfg.HEIGHT - y

    obj.save()
    obj.set_line_width(6.0)
    obj.arc(x, y, 10, 0, 2 * 3.14)
    obj.stroke_preserve()
    obj.set_source_rgb(0, 0.2, 0.8)
    obj.fill()
    obj.restore()


def create_holst():
    """ Создаёт полотно для рисование объектов """
    svg = SVGSurface(cfg.NAME_SVG, cfg.WIDTH, cfg.HEIGHT)
    holst = Context(svg)
    m = Matrix(yy=-1, y0=cfg.HEIGHT)
    holst.transform(m)
    holst.save()
    holst.set_source_rgb(0.3, 0.3, 0.05)
    holst.paint()
    holst.restore()
    return holst, svg


def save_png(svg: SVGSurface) -> None:
    if cfg.SAVE_PNG:
        svg.write_to_png(cfg.NAME_PNG)
    svg.finish()


def algorithm_graham(points:[int, int]):
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


def draw_line(obj: Context, x1: int, y1: int, x2: int, y2: int, color: int = 0, width: int = 5) -> None:
    y1 = cfg.HEIGHT - y1
    y2 = cfg.HEIGHT - y2
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


def draw_lines(holst, points):
    for i, v in enumerate(points):
        if points[i] == points[-1]:
            draw_line(holst, *points[0], *points[-1])
            break
        draw_line(holst, *v, *points[i + 1])


def draw_algorithm_graham(points):
    holst, svg = create_holst()
    result = algorithm_graham(points)
    for coord in points:
        draw_circle(holst, *coord)
    draw_lines(holst, result)
    save_png(svg)
