import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 14 Warehouse woes

def load_data(file_name):
    map = []
    moves = []

    with open(file_name, "r") as f:
        for line in f:
            line = list(line.strip())

            if len(line)==0:
                continue

            if any(a in line for a in ["#","0",".","@"]):
                map.append(line)

            elif any(a in line for a in ["v","^",">","<"]):
                moves.extend(line)
        
    return map, moves


# task 1:
#   - robot pushes boxes in warehouse with no care
#   - robot is @, boxes are O, walls are #
#   - moves are the 4 direction arrows ^,v,<,>, moves are a SINGLE, giant sequence
#   - box gps coordinate = 100 * distance from top wall + distance form left wall



def predict_robot_moves(map, moves):
    map_array = np.array(map)

    rows,cols = map_array.shape
    
    directions = {
        "v": np.array([1,0]),
        "^": np.array([-1,0]),
        ">": np.array([0,1]),
        "<": np.array([0,-1]),
    }
    
    # get all coords
    robot_coord = np.column_stack(np.where(map_array == "@"))[0]
    wall_coords = np.column_stack(np.where(map_array == "#"))

    for i, move in enumerate(moves):
        dir = directions[move]
        
        new_robot_coord = robot_coord + dir

        # if new coord is a wall, then stop directly
        if np.any(np.all(new_robot_coord == wall_coords,axis=1),axis=0):
            continue
        
        # if free space, then move on that
        if map_array[new_robot_coord[0],new_robot_coord[1]] == ".":

            # update map
            map_array[robot_coord[0],robot_coord[1]] = "."
            map_array[new_robot_coord[0],new_robot_coord[1]] = "@"

            # update coord of robot
            robot_coord = new_robot_coord
            continue
        
        # print(i, "moving box")
        if move == "v":
            sub_array = map_array[new_robot_coord[0]:rows, new_robot_coord[1]]
        elif move == "^":
            sub_array = map_array[1:robot_coord[0], new_robot_coord[1]][::-1]
        elif move == ">":
            sub_array = map_array[new_robot_coord[0], new_robot_coord[1]:cols]
        elif move == "<":
            sub_array = map_array[new_robot_coord[0], 1:robot_coord[1]][::-1]

        free_slots = np.where(sub_array==".")[0]

        # if free slot in the line
        if len(free_slots)!= 0:
            first_slot = free_slots[0]

            # there is a wall
            if np.any("#" == sub_array[0:first_slot]):
                continue

            new_box_coord = new_robot_coord + first_slot * dir
            
            # update map
            map_array[robot_coord[0],robot_coord[1]] = "."          # trail
            map_array[new_robot_coord[0],new_robot_coord[1]] = "@"  # robot
            map_array[new_box_coord[0],new_box_coord[1]] = "O"      # farthest box

            # update coord of robot
            robot_coord = new_robot_coord
        

    box_coords = np.column_stack(np.where(map_array == "O"))
    gps_sum = np.sum(box_coords* np.array([100,1]))

    return gps_sum

# task 2 
#   - everything except the robot is twice as wide # = ##, O= [], .=..
#   - means it could push 2 boxes at once

def wide_warehouse(map,moves):

    # wide map
    wide_map = []
    robot_coord = ()
    wall_coords = []
    empty_coords = []
    # box_left_coords = []
    # box_right_coords = []

    box_coords = {}

    # gen wide map and set coordinates of all the walls
    for i, row in enumerate(map):
        new_row = []
        for j, elem in enumerate(row):
            double_coords = [(i,j * 2),(i,j * 2+1)]
            if elem == "#":
                new_row.extend([elem]*2)
                wall_coords.extend(double_coords)
            elif elem == ".":
                new_row.extend([elem]*2)
                empty_coords.extend(double_coords)
            elif elem == "O":
                new_row.extend(["[","]"])
                box_coords[double_coords[0]] = "L"
                box_coords[double_coords[1]] = "R"
                # box_left_coords.append(double_coords[0])
                # box_right_coords.append(double_coords[1])
            elif elem == "@":
                new_row.extend(["@","."])
                robot_coord = double_coords[0]
                empty_coords.append(double_coords[1])
        wide_map.append(new_row)

    # get array
    wide_array= np.array(wide_map)
    rows,cols = wide_array.shape

    directions = {
        "v": (1,0),
        "^": (-1,0),
        ">": (0,1),
        "<": (0,-1),
    }

    for move in moves:

        # get dir to move
        dir = directions[move]
        
        # get next coord
        next_pos = (robot_coord[0] + dir[0], robot_coord[1] + dir[1])
        
        # hits a wall
        if next_pos in wall_coords:
            continue
        # no obstacle
        elif next_pos in empty_coords:
            index = empty_coords.index(next_pos)    # index of coord in empty coords
            empty_coords[index] = robot_coord       # update empty

            # update robot position
            robot_coord = next_pos  

        # 1 obstacle
        else:
            # get index of the box
            x,y = next_pos
            side = box_coords[(x,y)]
            sec_box = (x,y +1) if side =="L" else (x,y -1)
            
            # generate line of coords to check
            line = []

            # line = [(x+dir[0] * i,y + dir[1] * i) for i in range()]

            while 0 <= x < rows and 0 <= y < cols:
                line.append((x,y))

                # search one coord further
                x += dir[0]
                y += dir[1]
            
            # horizontal case
            if dir[1] != 0:

                free_slots = []

                for i, coord in enumerate(line):
                    if coord in wall_coords:
                        break
                    elif coord in empty_coords:
                        free_slots.append(True)
                    else:
                        free_slots.append(False)

                # can move
                if any(free_slots):
                    first_free_index = free_slots.index(True)
                    boxes_to_move = line[0:first_free_index+1]
                    # print(boxes_to_move)
                    for i,box in enumerate(boxes_to_move):
                        if i ==0:
                            box_coords.pop(box)
                            robot_coord = box
                        elif i < len(boxes_to_move) - 1:
                            box_coords[box] = "L" if box_coords[box] == "R" else "R"
                        else:
                            box_coords[box] = "R" if sum(dir) == 1 else "L"

                # cannot move because of wall
                else:
                    continue

            # vertical direction
            else:
                print(next_pos,sec_box)
                print(box_coords)


        

# RUN   


file_name = "data/example.txt"
# file_name = "data/dec-15.txt"

map, moves = load_data(file_name)

# tot_coords = predict_robot_moves(map, moves)
tot_coords = wide_warehouse(map,moves)
print(tot_coords)