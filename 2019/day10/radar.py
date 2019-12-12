#!python3

EMPTY_SYM = '.'
ASTEROID_SYM = '#'
LEFT=0
RIGHT=1
UP=2
DOWN=3

def greatest_common_div(a, b):
    while b:
        a, b = b, a%b
    return a


def count_visible_asteroids(m, x1, y1, WIDTH, HEIGHT):

    visible_count = 0
    
    for y2 in range(HEIGHT):
        for x2 in range(WIDTH):
            if m[y2][x2] != ASTEROID_SYM or y2 == y1 and x2 == x1: continue
            y_len, x_len = y2-y1, x2-x1
            common_div = abs(greatest_common_div(y_len, x_len))
            y_len //= common_div
            x_len //= common_div
            for step in range(1, common_div):
                if m[y1+y_len*step][x1+x_len*step] == ASTEROID_SYM:
                    break
            else:
                visible_count += 1

    return visible_count


def vaporize_asteroids(m, cannon_x, cannon_y, WIDTH, HEIGHT, vaporized_num):

    asteroids_by_quadrant_angle = dict()
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if m[y][x] == ASTEROID_SYM and (y, x) != (cannon_y, cannon_x):
                y_len, x_len = y-cannon_y, x-cannon_x 
                angle = -90 if (cannon_x == x or cannon_y == y) else y_len/x_len
                if x >= cannon_x and y < cannon_y:
                    quadrant = 0
                elif x > cannon_x and y >= cannon_y:
                    quadrant = 1
                elif x <= cannon_x and y > cannon_y:
                    quadrant = 2
                elif x < cannon_x and y <= cannon_y:
                    quadrant = 3
                asteroids_by_quadrant_angle.setdefault((quadrant, angle), []).append((y, x))

    for k in asteroids_by_quadrant_angle:
        asteroids_by_quadrant_angle[k] = sorted(
            asteroids_by_quadrant_angle[k],
            key=lambda point: ((cannon_y-point[0])**2+(cannon_x-point[1])**2)**0.5
        )

    vaporized_count, ret_val = 0, None

    while asteroids_by_quadrant_angle:

        for k in sorted(asteroids_by_quadrant_angle.keys()):

            if len(asteroids_by_quadrant_angle[k]) == 0:
                del(asteroids_by_quadrant_angle[k])
                continue

            y, x = asteroids_by_quadrant_angle[k].pop(0)

            vaporized_count += 1
            if vaporized_count == vaporized_num:
                ret_val = y, x
                asteroid_by_quadrant_angle = None
                break

    return ret_val

        
if __name__ == "__main__":

    with open("input.txt") as f:
        m = list(map(str.strip, f.readlines()))

    X, Y = len(m[0]), len(m)
    print(X, Y)

    visibility_map = [[0]*X for _ in range(Y)]

    for y in range(Y):
        for x in range(X):
            if m[y][x] == ASTEROID_SYM:
                visibility_map[y][x] = count_visible_asteroids(m, x, y, X, Y)

    coordinates, max_visible = None, 0
    for y in range(Y):
        for x in range(X):
            if visibility_map[y][x] > max_visible:
                max_visible, coordinates = visibility_map[y][x], (x, y)

    print(f"max visible asteroids: {max_visible} at {coordinates}.")
    y, x = vaporize_asteroids(m, coordinates[0], coordinates[1], X, Y, 200)
    print(f"result: {x*100+y}.")
