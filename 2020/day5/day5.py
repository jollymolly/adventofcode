#!python3

import sys


class SeatFinder:

    def __init__(self):
        self.seatId = None

    def __call__(self, boardingPass: str):

        row_num = self._binaryFinder(boardingPass[:7], 0, 127, 'F')
        col_num = self._binaryFinder(boardingPass[-3:], 0, 7, 'L')

        boardingPassSeatId = row_num * 8 + col_num
        
        if self.seatId is None or boardingPassSeatId > self.seatId:
            self.seatId = boardingPassSeatId

        return boardingPassSeatId

    @staticmethod
    def _binaryFinder(path: str, low: int, high: int, loCode: str) -> int:

        for ch in path:
            mid = (high - low) // 2

            if mid == 0:
                mid = low if ch == loCode else high
                continue
            
            if ch == loCode:
                high -= mid+1
            else:
                low += mid+1

        return mid
    

def main(args):

    if len(args) != 2:
        print(f"Cmd line: {args[0]} <input_file>")
        return 1

    seatFinder = SeatFinder()
    
    with open(args[1]) as inp:
        tuple(map(
            print, map(
                seatFinder, filter(
                    lambda s: s and len(s) == 10,map(str.strip, inp)
                )
            )
        ))
        
    print(f"Answer: {seatFinder.seatId}.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
