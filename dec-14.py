import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 14 restroom redoubt

def load_data(file_name):
    data = []

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()

            vals = re.findall("-*[0-9]+", line)
            robot = {
                "p": (int(vals[0]),int(vals[1])),
                "v": (int(vals[2]),int(vals[3]))
            }

            data.append(robot)
    return data


# Task 1:
#   - robots move in straight lines
#   - robots positions: p=x,y and velocities: v = x,y (per second)
#   - p=0,0 is top left corner (top down view)
#   - area is 101 wide and 103 tall, example is 11 wide and 7 tall
#   - robots can be piled on the same tile but teleport to the other side when hit an edge
#   - get pos of robots after 100 seconds, then count # of robots in each quadrant (middle row and col don't count as quadrant)
#   - then multiply quadrants together



def predict_robots_pos(data, seconds):

    # setup map
    cols = 101
    rows = 103

    for i in range(seconds):
        for j, robot in enumerate(data):
            x,y = (robot["p"][0]+robot["v"][0], robot["p"][1]+robot["v"][1])
            
            # teleport x
            if x < 0:
                x += cols
            elif x >= cols:
                x -= cols
            
            # teleport y
            if y < 0:
                y += rows
            elif y >= rows:
                y -= rows

            data[j]["p"] = (x,y)

    mid_col = cols // 2
    mid_row = rows // 2

    # each quadrant has 4 coords: (start_col,start_row,end_col,end_row)
    quadrants = {1: (0,0,mid_col,mid_row),
                 2: (mid_col+1,0,cols,mid_row),
                 3: (0,mid_row+1,mid_col,rows),
                 4: (mid_col+1,mid_row+1,cols,rows)}
    
    robot_per_quad = {i:0 for i in range(1,5)}

    # count robots in each quadrant
    for robot in data:
        x,y = robot["p"]

        for key, (i,j,k,l) in quadrants.items():
            
            if i<= x <k and j <=y < l:
                robot_per_quad[key]+= 1

    # compute safety factor
    prod = 1
    for val in robot_per_quad.values():
        prod *= val

    return prod




# part 2:
#   - after how many seconds it forms a christmas tree picture??

import cv2

def find_easter_egg(data):
    # setup map
    cols = 101
    rows = 103
    # cols = 11
    # rows = 7


    # start_x, start_y, end_x, end_y
    a,b,c,d = (cols //3, rows//3, 2* cols//3, 2*rows//3)

    def check_array(picture, iter):

        h_distrib = np.sum(picture,axis=0) # Sum of 1s across columns
        v_distrib = np.sum(picture,axis=1) # Sum of 1s across rows        

        # compute variance
        h_var = np.var(h_distrib, axis=0)
        v_var = np.var(v_distrib, axis=0)

        if (h_var> 20 and v_var >20) :

            # cv2.imshow("lol",picture)
            # cv2.waitKey(1)
            #             
            cv2.imwrite(f"imgs/{iter +1}.png",picture*255)
            return True
        return False

    
    iter = 0

    for i in tqdm(range(100000)):
    # for i in (range(10000)):
        picture = np.zeros((rows,cols))

        for j, robot in enumerate(data):
            x,y = (robot["p"][0]+robot["v"][0], robot["p"][1]+robot["v"][1])
            
            # teleport x
            if x < 0:
                x += cols
            elif x >= cols:
                x -= cols
            
            # teleport y
            if y < 0:
                y += rows
            elif y >= rows:
                y -= rows

            data[j]["p"] = (x,y)
            picture[y][x] += 1

        is_tree = check_array(picture, i)

        if is_tree:
            iter = i
            break
        
    
    return iter + 1
# RUN   


file_name = "data/example.txt"
file_name = "data/dec-14.txt"

data = load_data(file_name)

# safety_factor = predict_robots_pos(data, 100)
# print(safety_factor)

seconds = find_easter_egg(data)
print(seconds)

