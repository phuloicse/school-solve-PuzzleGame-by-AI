import os
import time
import resource
from os import listdir
from os.path import isfile, join
import ntpath


from Tents.tents_solver import Tents

input_path = os.path.join(os.curdir, "input")
output_path = os.path.join(os.curdir, "output")
for puzzle_dir_name in os.listdir(input_path):
    puzzle_dir_path = os.path.join(input_path,puzzle_dir_name)
    onlyfiles = [os.path.join(puzzle_dir_path,f) for f in listdir(puzzle_dir_path) if isfile(join(puzzle_dir_path, f))]
    for file in onlyfiles:
        print(f"Input file: {file}")
        # Init game and counter
        game = Tents(str(file))
        time_start = time.perf_counter()
        resource_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        # Solve the game
        game.solve()

        # Read the counter values and substract
        time_elapsed = (time.perf_counter() - time_start)
        resource_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - resource_before

        # Calculate output path
        overriden_output_path = os.path.join(output_path,puzzle_dir_name,ntpath.basename(file))
        game.print_solution(auto_output_path=overriden_output_path)

        print(f"Will save in: {overriden_output_path}")

    # for puzzle_dir in lisdir:
    # puzzle_dir_path = os.path.join(puzzle_dir,"")



