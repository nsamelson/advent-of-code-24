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

    # recursively push boxes
    def push_boxes(box_1, direction, visited):
        x_1,y_1 = box_1
        dx, dy = direction

        

        # compute both adjacent boxes
        next_box_1 = (x_1 + dx, y_1 + dy)
        

        if box_1 in visited:
            # print(visited)
            print("Already visited, breaking recursion")
            return False
        
        visited.add(box_1)
        
        # Base case: stop if any of the 2 boxes hits a wall or another box with no space
        if (next_box_1 in wall_coords) \
            or (next_box_1 in box_coords and not can_push(next_box_1, direction)):
            
            return False
        
        if box_1 in empty_coords:
            print("Found empty space at: ", box_1)
            return True
        
            
        # # Move the box if there's space
        # if next_box_1 in empty_coords:
        #     print("Found empty spaces for: ", box_1, "in ", next_box_1)
        #     return True
        
        # get sibling box too 
        side = box_coords[box_1]
        box_2 = (box_1[0], box_1[1] + 1 if side == "L" else box_1[1] - 1)
        x_2,y_2 = box_2
        next_box_2 = (x_2 + dx, y_2 + dy)

        # Recursive case: push the next box and then move the current one
        if next_box_1 in box_coords:
            print("Attempting to push:", box_1, box_2, "->", next_box_1, next_box_2)

            can_move_1 = True if next_box_1 == box_2 else push_boxes(next_box_1, direction, visited)
            can_move_2 = push_boxes(next_box_2, direction, visited) 

            if can_move_1 and can_move_2:   
                # if next_box_1 == box_2:
                box_coords[next_box_2] = box_coords.pop(box_2)  
                box_coords[next_box_1] = box_coords.pop(box_1) 

                # update empty coords
                if next_box_2 in empty_coords:
                    empty_coords[empty_coords.index(next_box_2)] = box_2 
                if next_box_1 in empty_coords:
                    empty_coords[empty_coords.index(next_box_1)] = box_1  

                visited.add(box_1)
                visited.add(box_2)

                return True
            else:
                return False
            
        # TODO: there is a case I didn't take into account!!!!
        if box_1 in box_coords and next_box_1 in empty_coords:

            if push_boxes(next_box_2, direction, visited) :
                box_coords[next_box_1] = box_coords.pop(box_1) 
                empty_coords[empty_coords.index(next_box_1)] = box_1 
                
                print("Pushing ",box_1, box_2, "to ", next_box_1,next_box_2)
            return True
        
        print("out", box_1, next_box_1, box_coords)

        return False
        
    # Helper function to check if a box can be pushed
    def can_push(coord, direction):
        x, y = coord
        dx, dy = direction
        while 0 <= x < rows and 0 <= y < cols:
            x, y = x + dx, y + dy
            if (x, y) in wall_coords:
                return False
            if (x, y) in empty_coords:
                return True
        return False
    
    for move in moves:
        dx, dy = directions[move]
        next_pos = (robot_coord[0] + dx, robot_coord[1] + dy)

        # print(move, robot_coord, next_pos,box_coords)

        # Wall block
        if next_pos in wall_coords:
            continue

        # Empty space
        elif next_pos in empty_coords:  
            empty_coords[empty_coords.index(next_pos)] = robot_coord
            robot_coord = next_pos

        # Box interaction
        elif next_pos in box_coords:    
            if push_boxes(next_pos, (dx, dy),set()):
                robot_coord = next_pos
                
        print(move, robot_coord, box_coords)
        # break
  

        

# RUN   


file_name = "data/example.txt"
# file_name = "data/dec-15.txt"

map, moves = load_data(file_name)

# tot_coords = predict_robot_moves(map, moves)
tot_coords = wide_warehouse(map,moves)
print(tot_coords)