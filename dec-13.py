import numpy as np
from tqdm import tqdm
import itertools
import re

# DAY 13 claw machines

def load_data(file_name):
    data = []
    machine = {}

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()

            if len(line) == 0:
                # machine = {}
                continue

            coords = re.findall("[0-9]+", line)

            if "Button A:" in line:
                machine["A"] = tuple(int(x) for x in coords)
            elif "Button B:" in line:
                machine["B"] = tuple(int(x) for x in coords)
            else:
                machine["G"] = tuple(int(x) for x in coords)
            
            if len(machine.keys()) == 3:
                data.append(machine)
                machine = {}
            

    return data


# task 1:
#   - 2 buttons machines (A and B)
#   - costs 3 token to push A, and 1 to push B
#   - each machine's buttons configed to move the claw to the right(x) and forward (y)
#   - each machine has a prize at exact coordinates to get it
# what smallest number of tokens to spend to win as many prizes

def claw_machines(machines):
    all_tokens = 0

    for machine in machines:

        a_x, a_y = machine["A"]
        b_x, b_y = machine["B"]
        goal_x, goal_y = machine["G"]

        # isolate j then use it to find i
        j = (goal_y * a_x - goal_x * a_y ) / (b_y * a_x - b_x * a_y)
        i = (goal_y - j * b_y) / a_y

        if float(i).is_integer() and float(j).is_integer(): # DONT FORGET PARENTHESIS AAAAAAAA
            if i <= 100 and j <= 100:
                all_tokens += 3 * i + j

    return all_tokens

# part 2:
#   - goal is goal + 10000000000000 

def claw_machines_big(machines):
    all_tokens = 0

    for machine in machines:

        a_x, a_y = machine["A"]
        b_x, b_y = machine["B"]
        goal_x, goal_y = (machine["G"][0] + 10000000000000, machine["G"][1] + 10000000000000)

        # isolate j then use it to find i
        j = float((goal_y * a_x - goal_x * a_y ) / (b_y * a_x - b_x * a_y))
        i = float((goal_y - j * b_y) / a_y)

        if i.is_integer() and j.is_integer():
            # if i <= 100 and j <= 100:
            all_tokens += 3 * i + j        

    return all_tokens

# RUN


file_name = "data/example.txt"
file_name = "data/dec-13.txt"

data = load_data(file_name)

# print(data[-1])

# tokens = claw_machines(data)
tokens = claw_machines_big(data)
print(tokens)
