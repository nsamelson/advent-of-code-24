import numpy as np
from tqdm import tqdm
import itertools
import re


# day 8

regex = "[a-zA-Z0-9]"

def load_data(file_name):
    map = []
    antennas = set()

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            map.append(list(line))

            types = re.findall(regex,line)
            antennas.update(types)

    return map, antennas


# task 1:
#   - detect antennas that could be [a~A,z~Z] and also [0-9]
#   - each paired antenna creates 0-2 antinodes, at same distance as those antennas, aligned
#   - single antenna doesn't create antinode
#   - antinodes can overlap with antenas, but not 2 antinodes on the same location


def find_antinodes(map_data,antenna_types):

    map_array = np.array(map_data)
    map_shape = map_array.shape

    antinodes = set()
    antennas = {ant: np.column_stack(np.where(map_array == ant)) for ant in antenna_types}

    for antenna_type, coords in antennas.items():

        # find at least 2 to create a pair and gen antinodes
        if len(coords) > 1:
            pairs = itertools.combinations(coords,2)
            
            for coord_1, coord_2 in pairs:
                distance = coord_2 - coord_1
                antinode_1 = coord_1 - distance
                antinode_2 = coord_2 + distance
                # print(antenna_type, coord_1, coord_2, antinode_1, antinode_2)
                
                # check bounds of map
                if 0 <= antinode_1[0] < map_shape[0] and 0 <= antinode_1[1] < map_shape[1]:
                    antinodes.add(tuple(antinode_1))

                if 0 <= antinode_2[0] < map_shape[0] and 0 <= antinode_2[1] < map_shape[1]:
                    antinodes.add(tuple(antinode_2))
    
    return len(antinodes)

# task 2:
#   - antinodes reapeatedly created at each distance of the 2 nodes 

def find_resonant_antinodes(map_data,antenna_types):

    map_array = np.array(map_data)
    map_shape = map_array.shape

    antinodes = set()
    antennas = {ant: np.column_stack(np.where(map_array == ant)) for ant in antenna_types}

    def is_within_bounds(coord):
        return 0 <= coord[0] < map_shape[0] and 0 <= coord[1] < map_shape[1]

    for antenna_type, coords in antennas.items():

        # find at least 2 to create a pair and gen antinodes
        if len(coords) > 1:            
            for coord_1, coord_2 in itertools.combinations(coords,2):
                distance = coord_2 - coord_1
                antinode_1 = coord_1 - distance
                antinode_2 = coord_2 + distance

                # start with antenna positions
                antinodes.add(tuple(coord_1))
                antinodes.add(tuple(coord_2))
                
                # check bounds of map
                while is_within_bounds(antinode_1):
                    antinodes.add(tuple(antinode_1))
                    antinode_1 -= distance

                while  is_within_bounds(antinode_2):
                    antinodes.add(tuple(antinode_2))
                    antinode_2 += distance
    

    return len(antinodes)



# RUN

file_name = "data/example.txt"
file_name = "data/dec-8.txt"

map_data, antennas = load_data(file_name)

antinodes = find_antinodes(map_data,antennas)
resonant_antinodes = find_resonant_antinodes(map_data,antennas)
print(resonant_antinodes)