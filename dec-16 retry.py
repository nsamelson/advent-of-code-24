import math
import numpy as np
from tqdm import tqdm
import itertools
import re
import heapq


# DAY 16 Reindeer maze

def load_data(file_name):
    map = [list(line.strip()) for line in open(file_name, "r").readlines()]        
    return map

# tasks:
#   - find lowest path score
#   - start marked S and end marked E, deer facing east
#   - moving 1 forward = 1 point, rotating 90° = 1000 points

def maze_bfs(map):
    map_array = np.array(map)
    start = tuple(np.argwhere(map_array == "S")[0])

    def rotate(direction, rot):
        dx, dy = direction
        return (dx * rot[0] + dy * rot[1], dx * rot[2] + dy * rot[3])

    rotate_right = (0, 1, -1, 0)  # Flattened matrix for rotation
    rotate_left  = (0, -1, 1, 0)
    
    visited = set()
    queue = [( 0, start, (0,1))]
    heapq.heapify(queue)

    while queue:
        score, (x,y), dir = heapq.heappop(queue)

        if (x,y, dir) in visited:
            continue
        visited.add((x,y, dir))
        
        if map_array[x,y] == "E":
            return score
        
        # forward
        nx,ny = (x +dir[0], y + dir[1])
        if map_array[nx,ny] != "#":
            heapq.heappush(queue, (score +1,(nx,ny), dir))

        # rotate left and right
        heapq.heappush(queue, (score + 1000, (x, y), rotate(dir,rotate_right)))
        heapq.heappush(queue, (score + 1000, (x, y), rotate(dir,rotate_left)))

    return None

# Task 2: skibidi toilet
#   - every non-wall tile is equipped with seat
#   - want to find count number of seats the path takes?

def comfy_maze_bfs(map):
    map_array = np.array(map)
    start = tuple(np.argwhere(map_array == "S")[0])

    def rotate(direction, rot):
        dx, dy = direction
        return (dx * rot[0] + dy * rot[1], dx * rot[2] + dy * rot[3])

    rotate_right = (0, 1, -1, 0)  # Flattened matrix for rotation
    rotate_left  = (0, -1, 1, 0)
    
    visited = set()
    queue = [( 0, start, (0,1), [])] # score, pos, dir, path
    heapq.heapify(queue)

    min_score = math.inf
    best_path = set()
    visited_paths = {}

    while queue:
        score, (x,y), dir, path = heapq.heappop(queue)
        
        if map_array[x,y] == "#":
            continue

        if score > min_score:
            continue
        
        if (x,y, dir, tuple(path)) in visited:
            continue

        visited.add((x,y, dir, tuple(path)))
        path.append((x,y))
        
        if map_array[x,y] == "E":
            min_score = min(min_score, score)
            visited_paths[tuple(visited)] = score
            
            if score == min_score:
                best_path.update(path)
                continue
            else:
                break


        # forward
        heapq.heappush(queue, (score +1,(x +dir[0], y + dir[1]), dir, path.copy()))
        # rotate left and right
        heapq.heappush(queue, (score + 1000, (x, y), rotate(dir,rotate_right), path.copy()))
        heapq.heappush(queue, (score + 1000, (x, y), rotate(dir,rotate_left), path.copy()))

    
    return min_score, len(best_path)


# RUN   


file_name = "data/example.txt"
# file_name = "data/dec-16.txt"

map = load_data(file_name)
# score = maze_bfs(map)
score = comfy_maze_bfs(map)

print(score)

