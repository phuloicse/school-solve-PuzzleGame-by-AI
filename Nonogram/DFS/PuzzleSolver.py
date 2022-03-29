from multiprocessing.connection import wait
from typing import List

from Nonogram.draw_nono_grams_board import draw_nono_board
from PuzzleState import PuzzleState as State
from Constraints import Constraints
from Permutation import Permutation
import copy
import time


class PuzzleSolver:
    def __init__(self, constraints: Constraints) -> None:
        self.constraints: Constraints = constraints
        self.permutation: Permutation = Permutation(constraints)
        self.counter = 1

    def _depth_first_search(self, row: int) -> None:
        self.nodes += 1
        if row > self.max_row:
            self.max_row = row
            print("Row: {}, nodes: {}, nodes/s: {:.2f}".format(self.max_row, self.nodes,
                                                               self.nodes / (time.perf_counter() - self.start_time)))
        print(self.state)
        time.sleep(0.2)

        if not self.state.validate(row):
            return

        if row + 1 == self.constraints.height:
            self.solutions.append(copy.deepcopy(self.state))
            print("Done " + str(self.counter) + "th solution")
            self.counter += 1
            return

        # print(self.state)

        for perm in self.permutation.get_permutations(row + 1):
            self.state.set_row(row + 1, perm)
            self._depth_first_search(row + 1)

        self.state.set_row(row + 1, [None for _ in range(self.constraints.width)])

    def save_state_as_img(self):
        from Nonogram.draw_nono_grams_board import draw_nono_board
        draw_nono_board(self.state)

    def solve(self) -> List[State]:
        self.state: State = State(self.constraints)
        self.solutions: List[State] = []
        self.nodes = -1
        self.max_row = 0
        self.start_time = time.perf_counter()
        self._depth_first_search(-1)
        return self.solutions
