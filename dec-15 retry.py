import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 15 Warehouse woes

def load_data(file_name):
    map = [list(line.strip()) for line in open(file_name, "r").readlines() if "#" in line]
    moves = [item for item in open(file_name, "r").read() if item in ["^","v","<",">"]]
        
    return map, moves


# task 1:
#   - robot pushes boxes in warehouse with no care
#   - robot is @, boxes are O, walls are #
#   - moves are the 4 direction arrows ^,v,<,>, moves are a SINGLE, giant sequence
#   - box gps coordinate = 100 * distance from top wall + distance form left wall



def predict_robot_moves(map, moves):
    map_array = np.array(map)
    pos = np.argwhere(map_array=="@")[0]
    
    directions = {
        "v": np.array([1,0]),
        "^": np.array([-1,0]),
        ">": np.array([0,1]),
        "<": np.array([0,-1]),
    }

    def project_next_pos(next_pos,dir):
        x,y = next_pos[0], next_pos[1]
        # hit wall
        if map_array[x,y] == "#":
            return None
        # free to go
        elif map_array[x,y] == ".":
            return next_pos
        # hit a box
        else:
            return project_next_pos(next_pos + dir, dir)

    for move in moves:
        dir = directions[move]
        new_pos = pos + dir
        
        next_free_pos = project_next_pos(new_pos, dir)

        # hit wall
        if next_free_pos is None:
            continue
        
        # box needs to be pushed
        if (next_free_pos!=new_pos).any():
            map_array[next_free_pos[0], next_free_pos[1]] = "O"  # place box on next_free_pos

        # set tail to free and new robot pos
        map_array[pos[0], pos[1]] = "."
        map_array[new_pos[0], new_pos[1]] = "@"

        # update pos
        pos = new_pos
    

    print(map_array)
    
    # compute GPS coordinates
    box_coords = np.argwhere(map_array=="O")
    gps_sum = sum([x * 100 +y for x,y in box_coords])

    
    return gps_sum


# task 2 
#   - everything except the robot is twice as wide # = ##, O= [], .=..
#   - means it could push 2 boxes at once

def wide_warehouse(map,moves):

    pass
        

# RUN   


file_name = "data/example.txt"
file_name = "data/dec-15.txt"

map, moves = load_data(file_name)


tot_coords = predict_robot_moves(map, moves)
print(tot_coords)
# tot_coords = wide_warehouse(map,moves)
# print(tot_coords)