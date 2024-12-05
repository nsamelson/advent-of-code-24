import numpy as np
# DAY FIVE



def load_data(file_name):
    ordering_rules = []
    updates_list = []
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if "|" in line:
                numbers = [int(num) for num in line.split("|")]
                ordering_rules.append((numbers))
            elif "," in line:
                numbers = [int(num) for num in line.split(",")]
                updates_list.append(numbers)
    return ordering_rules, updates_list


# Task 1:
#   - pages must be printed in a very specific order
#   - X|Y means that if need to update, page number X must be printed at some point before page number Y.
#   - page ordering rules and the pages to produce in each update (puzzle input)
#   - first section is page ordering rules X|Y
#   - second specifies the page numbers of each update
#   - identify which update is already in the right order
#   - also need to know the middle page number of each CORRECT UPDATE then sum them

def find_correct_updates(ordering_rules, updates):
    summed_pages = 0
    corrupt_updates = []

    # setup ordering rules dict
    rules = {}
    for rule in ordering_rules:
        if rule[0] not in rules.keys():
            rules[rule[0]] = [rule[1]]
        else:
            rules[rule[0]].append(rule[1])

    for update in updates:
        is_update_corrupt = False

        for i,page in enumerate(update):

            previous_pages = update[0:i] # from the update

            # check if there is a rule for this page and there were other pages before
            if page in rules.keys() and previous_pages != []:
                
                subsequent_pages = rules[page] # from the rules

                if any(x in previous_pages for x in subsequent_pages):
                    is_update_corrupt = True
                    corrupt_updates.append(update)
                    break
        
        if not is_update_corrupt:
            summed_pages += update[len(update)//2]
                
                # print(previous_pages)
    return summed_pages, corrupt_updates
            
# Task 2:
#   - fix the corrupt ones
#   - for the corrupt, use the page ordering rules to put them in the right order
#   - sum the incorrectly ordered ones's middle number and sum

def reorder_corrupted(ordering_rules, corrupt_updates):
    summed_pages = 0

    # setup ordering rules dict
    rules = {}
    for rule in ordering_rules:
        if rule[0] not in rules.keys():
            rules[rule[0]] = [rule[1]]
        else:
            rules[rule[0]].append(rule[1])


    for update in corrupt_updates:       

        i = 0
        while i < len(update):
            page = update[i]

            # check if there is a rule for this page and there were other pages before
            if page in rules.keys() and update[0:i] != []:
                
                rule_pages = rules[page] # from the rules

                # find indices in the update where number with a rule_pages is in the update list
                indices = [j for j, x in enumerate(update[0:i]) if x in rule_pages]
                
                if len(indices) != 0:

                    # switch elements
                    update[i] = update[min(indices)] 
                    update[min(indices)] = page

                    i = min(indices) # roll back to check if all good
                else:
                    i += 1
            else:
                i += 1
                
        # when quitting the while, not corrupt anymore
        summed_pages += update[len(update)//2]
                
    return summed_pages

# RUN

file_name = "data/example.txt"
file_name = "data/dec-5.txt"


ordering_rules, updates_list = load_data(file_name)
# print(ordering_rules, updates_list)

output, corrupt_updates = find_correct_updates(ordering_rules, updates_list)
corrupt_out = reorder_corrupted(ordering_rules, corrupt_updates)


print(output)
print(corrupt_out)