
import numpy as np
from tqdm import tqdm

# DAY SIX

def load_data(file_name):
    map_data = []
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            map_data.append(list(line))
           
    return map_data

# Task:
#   - guard is noted as ^ to face up, v, <, > for other dirs
#   - obstructions noted as #
#   - guards follow pattern of: 
#       - if something direct in front of you, turn 90° to the right
#       - else, step forward
#       - continues until leaving the map
#   - when guard passes on a point, mark as an X to later count the distinct positions 

def compute_pathing(map_data):
    
    guard = {
        "v":(1,0),
        "^":(-1,0),
        "<":(0,-1),
        ">":(0,1)
    }

    rotation_matrix = np.array([[0, 1],[-1, 0]]) # turn 90 degrees to the right
    obstacle = "#"
    path = "."

    map_array = np.array(map_data)
    map_shape = map_array.shape

    positions = {
        "guard": [],
        "obstacles": [],
        "path_points":[]
    }

    for i,line in enumerate(map_data):
        path_points = [(i,j) for j,x in enumerate(line) if x == path]
        obstacles = [(i,j) for j,x in enumerate(line) if x == obstacle]
        guard_pos = [(i,j) for j,x in enumerate(line) if x in guard.keys()]

        positions["path_points"].extend(path_points)
        positions["obstacles"].extend(obstacles)
        positions["guard"].extend(guard_pos)
        positions["path_points"].extend(guard_pos) # starting pos needs to be added

    # check the guard is well in the bounded map and continue the trajectory
    while all(x < y for x,y in zip(positions["guard"][-1], map_shape)) and all(x > y for x,y in zip(positions["guard"][-1], (0,0))):

        # compute new_position
        guard_dir = guard[map_array[positions["guard"][-1]]]
        new_pos = tuple(sum(i) for i in zip(positions["guard"][-1],guard_dir))
        

        # print(guard_dir, new_pos)

        if new_pos in positions["path_points"]:
            # update map
            map_array[new_pos] = map_array[positions["guard"][-1]] 
            map_array[positions["guard"][-1]] = "X"

            positions["guard"].append(new_pos) # update guard pos in dict


        elif new_pos in positions["obstacles"]:
            rotate_guard = np.matmul(rotation_matrix, np.array(guard_dir)) 
            guard_dir = list(guard.keys())[list(guard.values()).index(tuple(rotate_guard))] # change dir

            map_array[positions["guard"][-1]] = guard_dir
        else:
            break

    
    return positions

# Task 2:
#   - add an obstacle to put the guard in a loop

# def compute_obstacles(map_data):
#     new_obstacles = 0
#     rotation_matrix = np.array([[0, 1],[-1, 0]]) # turn 90 degrees to the right
#     map_shape = np.array(map_data).shape

#     obstacle = "#"
#     path = "."
#     guard = {
#         "v":(1,0),
#         "^":(-1,0),
#         "<":(0,-1),
#         ">":(0,1)
#     }

#     path_points = []
#     obstacles = []
#     guard_pos = []
#     for i,line in enumerate(map_data):
#         path_points.extend([(i,j) for j,x in enumerate(line) if x == path])
#         obstacles.extend([(i,j) for j,x in enumerate(line) if x == obstacle])
#         guard_pos.extend([(i,j) for j,x in enumerate(line) if x in guard.keys()])

#     # starting guard dir
#     guard_sign = map_data[guard_pos[0][0]][guard_pos[0][1]]
#     guard_dir = guard[guard_sign]
   

#     # set potential obstacles and add guard position as path_point
#     potential_obstacles = np.array(path_points.copy())
#     path_points = np.array(path_points.extend(guard_pos))
#     obstacles = np.array(obstacles)
#     guard_pos = np.array(guard_pos)

#     print("Obstacles to check: ",len(potential_obstacles))


#     def simulate_path(obstacle_set,guard_pos, guard_dir):
#         guard_dirs = np.array([guard_dir])
#         while all(x < y for x,y in zip(guard_pos[-1], map_shape)) and all(x > y for x,y in zip(guard_pos[-1], (0,0))):
#             # print(obstacle_set)

#             # compute next position
#             next_pos = guard_dir + guard_pos[-1]
            
#             # if encounter obstacle, rotate
#             if np.any(np.all(next_pos == obstacle_set, axis=1)):
#                 guard_dir = np.matmul(rotation_matrix,guard_dir)
            
#             # else, move the guard
#             else:
#                 guard_pos = np.concat((guard_pos, [next_pos]), axis=0)
#                 guard_dirs = np.concat((guard_dirs, [guard_dir]), axis=0)

#             # check if creates a loop
#             if len(guard_pos)>2:
#                 same_pos_check = np.where(np.all(guard_pos[-1] == guard_pos[:-1] , axis=1))[0]
#                 same_dir_check = np.where(np.all(guard_dir == guard_dirs[:-1], axis=1))[0]
                
#                 if len(same_pos_check)!=0:
#                     if any(np.isin(same_pos_check,same_dir_check)): # and np.any(same_pos_check == same_dir_check, axis=0):
#                         # print(np.in1d(same_pos_check,same_dir_check))
#                         # print(same_pos_check,same_dir_check)
#                         return True

#         return False

#     for i,new_obstacle in enumerate(tqdm(potential_obstacles)):
#         obstacle_set = np.concat((obstacles, [new_obstacle]), axis=0)
        
#         is_looping = simulate_path(obstacle_set,guard_pos,guard_dir)
#         if is_looping:
#             new_obstacles +=1
#             print(new_obstacle)
    
#     return new_obstacles

        
def compute_obstacles(map_data):
    rotation_matrix = np.array([[0, 1], [-1, 0]])  # turn 90 degrees to the right
    map_shape = np.array(map_data).shape
    obstacle = "#"
    path = "."
    guard = {"v": (1, 0), "^": (-1, 0), "<": (0, -1), ">": (0, 1)}

    # Collect positions
    path_points = []
    obstacles = set()
    guard_pos = None

    for i, line in enumerate(map_data):
        path_points.extend([(i, j) for j, x in enumerate(line) if x == path])
        obstacles.update([(i, j) for j, x in enumerate(line) if x == obstacle])
        if not guard_pos:
            guard_pos = [(i, j) for j, x in enumerate(line) if x in guard.keys()]

    guard_pos = guard_pos[0]
    guard_sign = map_data[guard_pos[0]][guard_pos[1]]
    guard_dir = guard[guard_sign]

    print("Obstacles to check: ", len(path_points))

    def simulate_path(obstacles, guard_pos, guard_dir):
        visited = set()
        guard_path = [guard_pos]
        direction = guard_dir

        while 0 <= guard_path[-1][0] < map_shape[0] and 0 <= guard_path[-1][1] < map_shape[1]:
            next_pos = (guard_path[-1][0] + direction[0], guard_path[-1][1] + direction[1])

            # If obstacle, rotate
            if next_pos in obstacles:
                direction = tuple(rotation_matrix @ np.array(direction))
            else:
                guard_path.append(next_pos)

            # Check for loops
            state = (guard_path[-1], direction)
            if state in visited:
                return True
            visited.add(state)

        return False

    new_obstacles = 0
    for new_obstacle in tqdm(path_points):
        obstacles.add(tuple(new_obstacle))
        if simulate_path(obstacles, guard_pos, guard_dir):
            new_obstacles += 1
        obstacles.remove(tuple(new_obstacle))

    return new_obstacles

   


# RUN

file_name = "data/example.txt"
file_name = "data/dec-6.txt"

map_data = load_data(file_name)

# positions = compute_pathing(map_data)
# print(len(set(positions["guard"])))


count_obstacle_positions = compute_obstacles(map_data)
print(count_obstacle_positions)