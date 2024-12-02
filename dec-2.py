import numpy as np

# DAY TWO: 



# init for test
reports_ex = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


file_name = "data/dec-2.txt"

def load_data(file_name):
    reports_matrix = []
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            numbers = line.split(" ")
            reports_matrix.append(np.array([int(num) for num in numbers]))
    # return np.array(reports_matrix)
    return reports_matrix

# Step 1: check if each report is safe
# Tasks:
#   - each line is only increasing or decreasing
#   - 2 adjacent numbers differ of : 1 <= diff <= 3


def check_reports(reports_list):
    safe_reports = 0
    for report in reports_list:
        diff = np.diff(report)
        
        # all are negatives = decreasing
        if (np.all(diff< 0) and np.all(diff> -4)) or (np.all(diff> 0) and np.all(diff< 4)):
            safe_reports += 1

    return safe_reports

# Step 2: check if each report is safe with a dampener
# Tasks:
#   - each line is only increasing or decreasing
#   - 2 adjacent numbers differ of : 1 <= diff <= 3
#   - 1 number can be removed in each report to make it safe

def check_reports_with_damp(reports_list):
    safe_reports = 0
    for report in reports_list:
        n = len(report)
        if n <= 2:  # Reports with 2 or fewer elements are always safe
            safe_reports += 1
            continue
        
        def is_safe(seq):
            diff = np.diff(seq)
            return ((np.all(diff > 0) and np.all(diff <= 3)) or 
                    (np.all(diff < 0) and np.all(diff >= -3)))

        if is_safe(report):  # If the report is already safe
            safe_reports += 1
            continue

        # Check if removing one number makes the report safe
        for i in range(n):
            new_report = np.delete(report, i)
            if is_safe(new_report):
                safe_reports += 1
                break    
        

    return safe_reports

# RUN
data = load_data(file_name)

print(check_reports(data))
print(check_reports_with_damp(data))