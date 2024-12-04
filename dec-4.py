import numpy as np

# DAT FOUR: word search "XMAS"

def load_data(file_name):
    lines = []
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            lines.append(list(line))
    return lines

# Task 1:
#   - find all the words "XMAS" in a table
#   - they can be horiz, vert, diag, backwards, overlapping


def word_search(data):
    puzzle = np.array(data)
    word_to_find = np.array(list("XMAS"))
    len_word = len(word_to_find)

    total_count = 0

    def check_line(line):
        return len([word_to_find for i in range(len(line)) if np.array_equal(line[i:i+len_word], word_to_find)])

    def check_by_line(matrix):
        count = 0
        for line in matrix:
            # left to right
            count += check_line(line)

            # right to left
            flipped = line[::-1]
            
            count += check_line(flipped)
        return count

    # horizontal check
    total_count += check_by_line(puzzle)

    # vertical check
    transposed = puzzle.transpose()
    total_count+= check_by_line(transposed)

    # diag check
    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            
            # top left to bottom right
            if i==0 or j ==0:
                diag_line_l = [puzzle[i+k][j+k] for k in range(min(puzzle.shape[0] - i,puzzle.shape[1] - j))]
                total_count += check_line(diag_line_l)

                flipped = diag_line_l[::-1]
                total_count += check_line(flipped)
                

            # top right to bottom left
            if i==0 or j == puzzle.shape[1] - 1: 
                diag_line_r = [puzzle[min(i+k,puzzle.shape[0]-1)][max(j-k,0)] for k in range(min(puzzle.shape[0] - i, j + 1)) ]
                total_count += check_line(diag_line_r)

                flipped = diag_line_r[::-1]
                total_count += check_line(flipped)

    return total_count






# RUN
file_name = "data/example.txt"
file_name = "data/dec-4.txt"

data = load_data(file_name)
count = word_search(data)
print(count)