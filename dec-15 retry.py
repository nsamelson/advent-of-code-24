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

def widen_map(map):
    new_map = []
    for row in map:
        new_row = []
        for item in row:
            if item == "O":
                new_row.extend(["[","]"])
            elif item == "@":
                new_row.extend([item,"."])
            else:
                new_row.extend([item]*2)
        new_map.append(new_row)
    
    return new_map

def wide_warehouse(map,moves):

    wide_map = widen_map(map)
    map_array = np.array(wide_map)
    pos = np.argwhere(map_array=="@")[0]
    
    directions = {
        "v": np.array([1,0]),
        "^": np.array([-1,0]),
        ">": np.array([0,1]),
        "<": np.array([0,-1]),
    }


    def project_next_pos(pos,dir, i ):

        x,y = pos
        next_pos = nx, ny = pos + dir
        type = str(map_array[x,y])
        next_type = str(map_array[nx, ny])

        sec_pos = sx,sy = pos + directions[">"] if type == "[" else pos + directions["<"]
        sec_next_pos = snx, sny = sec_pos + dir
        sec_type = str(map_array[sx,sy])
        next_sec_type = str(map_array[snx, sny])

        map_updates = {i:{
            (int(nx),int(ny)): type,            # move type to next location
            (int(x),int(y)): ".",               # setup trail
        }}
        
        # case of moving robot
        if type == "@":
            if next_type == "#":
                return False, map_updates
            
            elif next_type == ".":
                return True, map_updates
            
            else:
                # recursive call of first box part
                is_next_free, next_map_updates = project_next_pos(next_pos, dir, i+1)
                map_updates.update(next_map_updates) 
                return is_next_free, map_updates
        
        # case of moving boxes
        map_updates[i][(int(snx),int(sny))] = sec_type  # second box part
        
        if (next_pos != sec_pos).any():
            map_updates[i][(int(sx),int(sy))] = "."     # trail if not in map_update

        if next_type == "#" or next_sec_type == "#":    # hit wall
            return False, map_updates
        
        elif next_type == "." and next_sec_type == ".": # free to go
            return True, map_updates

        else:
            # push sideways
            if (next_pos == sec_pos).all():
                is_next_free, next_map_updates = project_next_pos(sec_next_pos, dir, i+1)
                map_updates.update(next_map_updates) 
                return is_next_free, map_updates
            
            else:
                if next_type in ["[","]"]:
                    is_first_free, a = project_next_pos(next_pos, dir, i+1)
                else:
                    is_first_free, a = True, {i+1:{}}
                
                if next_sec_type in ["[","]"]:
                    is_sec_free, b = project_next_pos(sec_next_pos, dir, i+1)
                else:
                    is_sec_free, b = True, {i+1:{}} 
                
                c = {}
                for d in (a, b):  
                    for k, v in d.items():  
                        c.setdefault(k, {}).update(v)

                map_updates.update(c) 

                return is_first_free and is_sec_free, map_updates
            


    i = 0
    for move in moves:
        dir = directions[move]
        # new_pos = pos + dir
        next_free_pos, map_updates = project_next_pos(pos, dir,0)
        

        # free to move
        if next_free_pos:
            for index in sorted(map_updates.keys(),reverse=True):
                for (x,y), type in map_updates[index].items():
                    map_array[x,y] = type

            pos += dir

            # if 19 <= i<= 22:
            # print(move, map_updates, next_free_pos)
            # print("\n".join(["".join(l) for l in map_array]))
        i+=1
    print("\n".join(["".join(l) for l in map_array]))

    # compute GPS coordinates
    l_box_coords = np.argwhere(map_array=="[")
    r_box_coords = np.argwhere(map_array=="]")

    gps_sum = sum([l_box_coords[i][0] * 100 + min(l_box_coords[i][1], r_box_coords[i][1]) for i in range(len(l_box_coords))])

    return gps_sum        

# RUN   


file_name = "data/example.txt"
# file_name = "data/dec-15.txt"

map, moves = load_data(file_name)


# tot_coords = predict_robot_moves(map, moves)
# print(tot_coords)
tot_coords = wide_warehouse(map,moves)
print(tot_coords)