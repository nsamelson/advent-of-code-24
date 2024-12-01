
# DAY ONE: Pairing up lists


# init for test
left_init = [3,4,2,1,3,3]
right_init = [4,3,5,3,9,3]


file_name = "data/dec-1.txt"

def load_data(file_name):
    left, right = [], []
    with open(file_name, "r") as f:
        for line in f:
            # clean and split into a list of 2 strings
            line = line.strip()
            ids = line.split("   ")
            
            # add to respective lists
            left.append(int(ids[0]))
            right.append(int(ids[1]))

    return left, right

# Step 1
# Tasks:
#   - pair the smallest number in the left and right list together, repeat with next smallest
#   - within each pair, check how far apart the numbers are (diff btween the two) 
#   - addup total distance

def pair_and_compute_distance(left, right):
    # sort
    sorted_left = sorted(left)
    sorted_right = sorted(right)
    total_dist = 0

    # compute distance for each sorted pair
    for i in range(len(left)):
        total_dist += abs(sorted_left[i] - sorted_right[i])

    return total_dist


# Step 2
# Tasks:
#   - Check how often each id from LEFT appears in RIGHT list
#   - calculate total similarity score by sum (number in LEFT * occurences in RIGHT)

def compute_similarity(left, right):
    total_similarity = 0

    # multiply the left number with the occurences in right
    for num in left:
        total_similarity += num * right.count(num)

    return total_similarity


# RUN
left_list,right_list = load_data(file_name)

print(pair_and_compute_distance(left_list,right_list))
print(compute_similarity(left_list,right_list))