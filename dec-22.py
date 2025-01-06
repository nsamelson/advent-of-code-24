from collections import deque
import heapq
import math
import numpy as np
from tqdm import tqdm
from itertools import chain, product
import re
from functools import cache

# DAY 22 Monkey market


def load_data(file_name):
    data = [int(line.strip() )for line in open(file_name).readlines()]

    return data


# task 1:
#   - sell good hiding spots to buy absurd amount of bananas
#   - buyers buy at pseudorandom prices: pseudorandom sequence of secret numbers where each secret is derived from the previous one
#   - process is: 
#       -- secret * 64, then XOR into the secret, then % 16777216
#       -- secret / 32, round to nearest integer, then XOR into the secret, then % 16777216
#       -- secret * 2048, then XOR into the secret, then % 16777216
#       -- gives the next secret number in the sequence

def decipher_secret(data):

    @cache
    def mix_and_prune(secret,value):
        return (secret ^ value) % 16777216

    total = 0
    for init in data: 
        secret = init
        for i in range(2000):
            secret = mix_and_prune(secret, secret*64)
            secret = mix_and_prune(secret, secret//32)
            secret = mix_and_prune(secret, secret*2048)

        # print(init, secret)
        total += secret

    return total




# RUN

file_name = "data/example.txt"
file_name = "data/dec-22.txt"

data = load_data(file_name)
# print(data)

out = decipher_secret(data)
print(out)