#!python3

import hal
import copy

BLACK_PAINT = '.'
WHITE_PAINT = '#'


class Robot:
    UP = 1
    DOWN = 3
    LEFT = 0
    RIGHT = 2

    TURN_LEFT_CODE = 0
    TURN_RIGHT_CODE = 1

    TURN_LOOP = (LEFT, UP, RIGHT, DOWN)
    TURN_LOOP_LEN = len(TURN_LOOP)
    DIRECTION_SYM = ('<', '^', '>', 'V')
    
    def __init__(self, instructions):
        self.brain = hal.ComputingUnit(instructions)
        self.turn_loop_idx = self.UP

    def go_paint(self, grid):

        x, y = grid.get_center_xy()
        grid_height, grid_width = grid.get_size()
        painted_panes = [[0]*grid_width for _ in range(grid_height)]

        while not self.brain.completed:

            self.brain.stdin = (0 if grid.get_panel_xy(x, y) == BLACK_PAINT else 1, )
            self.brain.execute()
            panel_color, turn_direction = self.brain.stdout[-2:]

            painted_panes[y][x] = grid.paint_panel_xy(x, y, BLACK_PAINT if panel_color == 0 else WHITE_PAINT)
            
            self.turn_loop_idx += 1 if turn_direction == self.TURN_RIGHT_CODE else -1
            self.turn_loop_idx = self.TURN_LOOP_LEN-1 if self.turn_loop_idx < 0 \
                else self.turn_loop_idx % self.TURN_LOOP_LEN
        
            if self.turn_loop_idx == self.UP or self.turn_loop_idx == self.DOWN:
                y += 1 if self.turn_loop_idx == self.DOWN else -1
            else:
                x += 1 if self.turn_loop_idx == self.RIGHT else -1

        print(f"painted once panes count: {sum(sum(row) for row in painted_panes)}.")
        

class Grid:
    HEIGHT = 100
    WIDTH = HEIGHT*2

    CENTER_X = WIDTH // 2
    CENTER_Y = HEIGHT // 2

    def __init__(self):
        self.grid = [[BLACK_PAINT for i in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.grid[self.CENTER_Y][self.CENTER_X] = WHITE_PAINT

    @staticmethod
    def get_center_xy():
        return Grid.CENTER_X, Grid.CENTER_Y

    def get_panel_xy(self, x, y):
        return self.grid[y][x]

    def paint_panel_xy(self, x, y, color):
        painted = 0
        if self.grid[y][x] != color:
            self.grid[y][x] = color
            painted = 1
        return painted

    @staticmethod
    def get_size():
        return Grid.HEIGHT, Grid.WIDTH

if __name__ == "__main__":

    instructions = []
    
    with open("input.txt") as f:
        instructions = list(map(int, f.readline().strip().split(",")))

    if not instructions:
        print( "No instructions provided, robot is of no use without brain.")

    hal.ComputingUnit.init_instruction_handlers()

    marvin = Robot(instructions)
    grid = Grid()
    marvin.go_paint(grid)
    for l in tuple("".join(line) for line in grid.grid):
        print(l)
