from sokoban import (
    Box,
    DOWN,
    Map,
    Player
)

from sokoban.gif import save_images, create_gif
from search_methods.ida_star import ida_star
from search_methods.heuristics import ida_heuristic, beam_search_heuristic
from search_methods.beam_search import beam_search
import sys
import os
import time

def run(algorithm, map_path):
    crt_map = Map.from_yaml(map_path)

    if algorithm == "ida*":
        print("Ruleaza IDA*\n")
        start_time = time.time()
        solution, num_states = ida_star(crt_map, heuristic=ida_heuristic)
        end_time = time.time()
    elif algorithm == "beam-search":
        print("Ruleaza Beam Search\n")
        start_time = time.time()
        solution, num_states = beam_search(crt_map, heuristic=beam_search_heuristic, beam_width=50)
        end_time = time.time()
    else:
        print(f"Algoritm necunoscut: {algorithm}")
        return

    if solution:
        print(f"Solutie gasita in {num_states} stari explorate, timp: {end_time - start_time:.2f} secunde\n")
        for move in solution:
            print(move)

        os.makedirs("images", exist_ok=True)
        step_maps = []
        current_map = crt_map.copy()

        for move in solution:
            step_maps.append(current_map.copy())
            current_map.apply_move(move)

        save_images(step_maps, "images")
        create_gif("images", "solution.gif", "images")
    else:
        print("Nu s-a gasit solutie!\n")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Nr incorect de atribute!")
        sys.exit(1)

    algorithm = sys.argv[1]
    map_path = sys.argv[2]

    run(algorithm, map_path)
