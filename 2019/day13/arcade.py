#!python3
import time


import hal

if __name__ == "__main__":

    instructions = None
    
    with open("input.txt") as f:
        instructions = list(map(int, f.readline().strip().split(',')))

    if not instructions:
        print("No insturctions to run.")
        
    hal.ComputingUnit.init_instruction_handlers()

    paddle_sym = hal.ComputingUnit.GraphicController.from_code(
        hal.ComputingUnit.GraphicController.HORIZONTAL_PADDLE_CODE
    )
    ball_sym = hal.ComputingUnit.GraphicController.from_code(
        hal.ComputingUnit.GraphicController.BALL_TILE_CODE
    )

    cu = hal.ComputingUnit(instructions)
    prev_input, paddle_line_num = None, None
    while not cu.completed:
        cu.execute()
        ball_line_num = None
        for line_idx, l in enumerate(cu.screen):
            if ball_line_num is None :
                ball_line_num = line_idx if ball_sym in l else None
            if paddle_line_num is None:
                paddle_line_num = line_idx if paddle_sym in l else paddle_line_num
            print(l)

        inp = '0'
        if ball_line_num < paddle_line_num:
            inp = '-1'
        elif ball_line_num > paddle_line_num:
            inp = '1'
        paddle_line_num += int(inp)
        cu.stdin = (inp, )
        prev_input = inp
        time.sleep(0.5)
        
    block_count = 0
    block_sym = hal.ComputingUnit.GraphicController.from_code(
        hal.ComputingUnit.GraphicController.BLOCK_TILE_CODE
    )
    for l in cu.screen:
        repr(l)
        block_count += l.count(block_sym)

    print(f"printed block tiles count: {block_count}.")
    
