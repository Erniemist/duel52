def point_inside(point, rect):
    px, py = point
    x, y, w, h = rect
    return x <= px <= x + w and y <= py <= y + h
