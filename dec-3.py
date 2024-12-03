import numpy as np
import re



# DAY THREE: 



def load_data(file_name):
    # corrupted_lines = []
    with open(file_name, "r") as f:
        file = f.read()
        # for line in f:
        #     line = line.strip()
        #     corrupted_lines.append(line)
    # return np.array(reports_matrix)
    return file

# Task 1: multiply some numbers
#   - mul(x,y), where x,y are 1-3 digit numbers
#   - invalid characters are ignored "*,!,?, ,..."
#   - add up correct multiplications


mull_seq = "mul\([0-9]*[0-9]*[0-9]\,[0-9]*[0-9]*[0-9]\)"
numbers_seq = "[0-9]*[0-9]*[0-9]"

def mull_it_over(corrupted):
    # find all the instructions
    mul_strings = re.findall(mull_seq, corrupted)

    # extract the numbers to multiply
    mul_numbers = [re.findall(numbers_seq, x) for x in mul_strings]
    product = [int(x[0])* int(x[1]) for x in mul_numbers]
        
    return sum(product)


# Task 2: filter muls
#   - do() instructions enables following mul instructions
#   - don't() instructions disable following mul instruction
#   - first mul() is enabled

enable_seq = r"do\(\)"
disable_seq = r"don't\(\)"

big_seq = r"mul\([0-9]*[0-9]*[0-9]\,[0-9]*[0-9]*[0-9]\)|do\(\)|don\'t\(\)"


def filter_with_orders(corrupted):
    total_sum = 0
    is_active = True

    all_strings = re.findall(big_seq,corrupted)

    for instr in all_strings:
        if re.search(mull_seq,instr) is not None and is_active:
            numbers = re.findall(numbers_seq, instr)
            total_sum += int(numbers[0]) * int(numbers[1])
        elif re.search(enable_seq,instr):
            is_active = True
        elif re.search(disable_seq,instr):
            is_active = False
    return total_sum


# RUN

file_name = "data/example.txt"
file_name = "data/dec-3.txt"

data = load_data(file_name)
total = mull_it_over(data)
print(total)

filtered = filter_with_orders(data)
print(filtered)

