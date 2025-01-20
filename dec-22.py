from collections import defaultdict, deque
import heapq
import math
# import numpy as np
# from tqdm import tqdm
from itertools import chain, product
import re
from functools import cache, lru_cache

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

# task 2:
#   - prices = ones digits of their secret numbers (3 from 123) = number of bananas
#   - our monkey sells only if 4 consecutive changes in price, and one sell per sequence
#   - only ONE sequence to use for all buyers, it can happen that there is no sequence for one of the buyers

def find_best_sequence(data):

    total = 0
    best_sequence = []
    sequences_dict = {}
    # all_sequences = dict.fromkeys(product(range(-9,10),repeat=4),{})
    all_sequences = defaultdict(dict)


    for i,secret in enumerate(data):

        # setup
        seq = deque(maxlen=4)
        last_price = None


        for _ in range(2000):
            
            # get last digit from secret
            price = secret % 10
            price_diff = price - last_price if last_price is not None else None

            # print(secret, price,last_price, price_diff)

            # generate sequence
            if price_diff is not None:
                seq.append(price_diff)

                # # remove first elem of seq # fifo
                # if len(seq)>4:
                #     seq.pop(0)
                
                if len(seq)==4:
                    seq_tuple = tuple(seq)
                    if i not in all_sequences[seq_tuple]:
                        all_sequences[tuple(seq)][i] = price
                
                # if len(seq)==4 and str(seq) not in sequences_dict[start_secret]:
                #     sequences_dict[start_secret][str(seq)] = price

            # generate new secret for next sequence
            secret = (secret ^ (secret<<6)) & 0xFFFFFF
            secret = (secret ^ (secret>>5)) & 0xFFFFFF
            secret = (secret ^ (secret<<11)) & 0xFFFFFF
            
            # update last price
            last_price = price

    # Now find best sequence
    # [ all_sequences.update(value.keys()) for key,value in sequences_dict.items()]
    print(all_sequences[(-2,1,-1,3)])

    return total
# RUN


file_name = "data/example.txt"
# file_name = "data/dec-22.txt"

data = load_data(file_name)
# print(data)

# out = decipher_secret(data)
out = find_best_sequence(data)
print(out)