#!python3


DIRECTION_LEFT = 'L'
DIRECTION_RIGHT = 'R'
DIRECTION_UP = 'U'
DIRECTION_DOWN = 'D'


def break_segment(segment):
    return segment[:1], int(segment[1:])

def segments_to_coordinates(wire):

    wire_segments_coords = list()
    x, y = 0, 0
    wire_segments_coords.append((x, y))
    for segment in wire:
        direction, length = break_segment(segment)

        if direction in (DIRECTION_LEFT, DIRECTION_RIGHT):
            x += length if direction == DIRECTION_RIGHT else -1 * length
        else:
            y += length if direction == DIRECTION_UP else -1 * length

        wire_segments_coords.append((x, y))

    return wire_segments_coords

def lines_intersect(line1, line2):

    intersection_coord = None

    if line1 == line2:
        intersection_coord = line1[0]
    elif (
            line1[0][1] == line1[1][1]  # when line2 intersect vertically
            and (
                line1[0][0] <= line2[0][0] and line2[0][0] <= line1[1][0]
                or line1[0][0] >= line2[0][0] and line2[0][0] >= line1[1][0]
            )
            and (
                line2[0][1] >= line1[0][1] and line2[1][1] <= line1[0][1]
                or line2[0][1] <= line1[0][1] and line2[1][1] >= line1[0][1]
            )
    ):
        intersection_coord = (line2[0][0], line1[0][1])
    elif (
            line1[0][0] == line1[1][0]  # when line2 intersect horizontally
            and (
                line1[0][1] <= line2[0][1] and line2[0][1] <= line1[1][1]
                or line1[0][1] >= line2[0][1] and line2[0][1] >= line1[1][1]
            )
            and (
                line2[0][0] >= line1[0][0] and line2[1][0] <= line1[0][0]
                or line2[0][0] <= line1[0][0] and line2[1][0] >= line1[0][0]
            )
    ):
        intersection_coord = (line1[0][0], line2[0][1])

    return intersection_coord

def sum_dots(dot1, dot2):
#    print(f"dots: {dot1} - {dot2}")
    return abs(dot2[0]-dot1[0]) + abs(dot2[1]-dot1[1])

def calculate_path(wire, idx):

    i, path = 1, 0

    while i < idx:
        path += sum_dots(wire[i-1], wire[i])
        i += 1

    return path
        

def wire_intersections(wire1, wire2):

    wire1_dots, wire2_dots = segments_to_coordinates(wire1), segments_to_coordinates(wire2)
    idx, end_idx = 1, len(wire1_dots)
    min_path = None
    while idx < end_idx:
        line1 = wire1_dots[idx-1], wire1_dots[idx]
        wire2_idx, wire2_end_idx = 2, len(wire2_dots)
        while wire2_idx < wire2_end_idx:
            line2 = wire2_dots[wire2_idx-1], wire2_dots[wire2_idx]

            intersection_coord = lines_intersect(line1, line2)
            if intersection_coord is not None:
                path_wire1 = calculate_path(wire1_dots, idx)+sum_dots(wire1_dots[idx-1], intersection_coord)
#                print(f"path_wire1: {path_wire1}")
                path_wire2 = calculate_path(wire2_dots, wire2_idx)+sum_dots(wire2_dots[wire2_idx-1], intersection_coord)
#                print(f"path_wire2: {path_wire2}")
                path = path_wire1 + path_wire2
                if min_path is None or path < min_path:
                    min_path = path

            wire2_idx += 1
        idx += 1

    return min_path


if __name__ == "__main__":

    wires_info_list = None
    with open("input_orig.txt") as f:
        wires_info_list = [line.strip().split(',') for line in f]

    if not wires_info_list or len(wires_info_list) != 2:
        print(f"wrong input data lenght: {len(wires_info_list) if wires_info_list is not None else 'None'}")
        
    print(f"Minimal path: {wire_intersections(wires_info_list[0], wires_info_list[1])}.")
       
