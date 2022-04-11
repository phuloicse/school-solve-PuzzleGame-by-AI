import os
import time
import resource
from os import listdir
from os.path import isfile, join
import ntpath
import json
from pathlib import Path
from solve import process_puzzle
# from PuzzleSolver import solve

input_path = os.path.join(os.curdir, "input")
# output_path = os.path.join(os.curdir, "output")
json_obj = []

for puzzle_dir_name in os.listdir(input_path):
    puzzle_dir_path = os.path.join(input_path, puzzle_dir_name)
    onlyfiles = [os.path.join(puzzle_dir_path, f) for f in listdir(
        puzzle_dir_path) if isfile(join(puzzle_dir_path, f))]
    total_mem_used = 0
    total_time_elapsed = 0
    for file in onlyfiles:
        print(f"Input file: {file}")
        # Init game and counter
        # game = Nono(str(file))
        
        time_start = time.perf_counter()
        resouce_test = 1
        save = process_puzzle(file)
        # try:
        #     # Solve the game
        #     game.solve()
        # except:
        #     print(f"Cannot solve puzzle {file}")
        # Read the counter values and substract
        time_elapsed = (time.perf_counter() - time_start)
        resource_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # Resource accumulator
        total_time_elapsed += time_elapsed
        total_mem_used += resource_used

        # Save the gaem stat
        game_stat = {"name": file, "time_used": time_elapsed,
                     "mem_used": resource_used, "steps": save}
        json_obj.append(game_stat)
        # Calculate output path
        # overriden_output_path = os.path.join(
        #     output_path, puzzle_dir_name, ntpath.basename(file))
        # pre, ext = overriden_output_path.rsplit(".", 1)
        # overriden_output_path = pre + ".png"
        # print(f" Path split is: {overriden_output_path.split()}")
        # game.print_solution(output_file_name=overriden_output_path,auto_output_path=overriden_output_path)


json_obj.append({"name":"total","time_used":total_time_elapsed,"mem_used":total_mem_used})
json_text = json.dumps(json_obj)

with open("Newdata.json", "w") as f:
    f.write(json_text)

    # for puzzle_dir in lisdir:
    # puzzle_dir_path = os.path.join(puzzle_dir,"")
