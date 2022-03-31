#!/bin/python3
import sys
import os
import json
from typing import List, Dict, Any
from Constraints import Constraints
from PuzzleSolver import PuzzleSolver as Solver
from PuzzleState import PuzzleState as State
import time
import resource
# import psutil
# sys.path.insert(0,'/mnt/f/OneDrive - hcmut.edu.vn/Using/School_Now/AI/BTL/solve-PuzzleGame-by-AI/Nonogram')
# import resource

def print_usage() -> None:
     print("Error, please try again on Linux or WSL. Try 'python3 solve.py  ./puzzles/(file name)' ")

def process_puzzle(path: str) -> int:
    """
    Processes one puzzle.
    The necessary steps are: Check the file, validate the contents, run the solver and 
    print the solutions, if any are found.
    """
    if not os.path.isfile(path):
        print("{} is not a regular file.".format(path))
        return

    try:
        f = open(path)
        json_object = json.load(f)
    except OSError as error:
        print("An error occurred while opening the file {}".format(path),
              file=sys.stderr)
        print(error.strerror, file=sys.stderr)
        return
    except json.JSONDecodeError as error:
        print("An error occurred while parsing the JSON file {}".format(path),
              file=sys.stderr)
        return
    else:
        f.close()

    errors, instance = Constraints.validate_json(json_object)
    # print(str(instance.columns))
    # print(str(instance.height))
    # print(str(instance.rows))
    # print(str(instance.width))
    if errors:
        print("The configuration file is not valid.", file=sys.stderr)
        print("Errors:", file=sys.stderr)
        print("\t", end="", file=sys.stderr)
        print("\n\t".join(errors), file=sys.stderr)
        return

    solver: Solver = Solver(instance)
    solutions: List[State] = solver.solve()
    
    """Print Solution and number of step used"""
    # print(solutions[0])
    # print(solutions[1])
    return solutions[1]
    # from Nonogram.draw_nono_grams_board import draw_nono_board
    # draw_nono_board(solutions[-1])

def main() -> None:
    if len(sys.argv) < 2 :
        print_usage()
        return
    # Start clock
    time_start = time.perf_counter()

    puzzles = len(sys.argv) - 1
    for index, path in enumerate(sys.argv[1:]):
        print("Processing puzzle {} of {}".format(index + 1, puzzles))
        process_puzzle(path)

    # End Clock and get mem usage: (can only run on linux or wsl on windows /docker with linux)
    time_elapsed = (time.perf_counter() - time_start)
    memB = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print("%5.7f secs %5.7f MB " % (time_elapsed, memB/1000))


if __name__ == "__main__":
    main()
# process_puzzle(test)

