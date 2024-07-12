#!/usr/bin/env python3

import random
from matplotlib import pyplot as plt
import numpy as np
from typing import Optional

class TabulationHash:
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the tabulation hash function.
        """
        #Implement a seed to get deterministic results
        if seed is not None:
            random.seed(seed)
        #Create a hash table that contains 4 smaller tables
        #Each table stores 2**16 random 32 bit numbers. We use 4 tables.
        self.hash_table = [[random.getrandbits(32) for _ in range(2**16)] for _ in range(4)]

    def __call__(self, x: np.uint64)->np.uint32:
        """
        Hash a 64-bit integer key x into 32-bit hash value
        """
        #We will split the 64 bit integer key x into 4 subkeys, each 16 bits long. Each 16 bit subkey will be used to index a unique value in one of the 4 arrays in the hash table. This was the reason the hash table contains 4 arrays and that each array contains 2**16 elements. 

        #Create a bit mask to select 16 bits ONLY from x
        #You can not perform logical and with numpy integer and integer
        bit_mask = np.uint32(0xffff)
        #Create a hash value. Initialize it to 0 for now.
        hash_value = 0

        for i in range(4):
            #You can not shift a numpy integer with an integer
            subkey = (x >> np.uint(i*16)) & bit_mask
            #Get the value in the hash table at the unique index of the subkey
            value = self.hash_table[i][subkey]
            #calculate the hash value using XOR operation between all the values
            hash_value = hash_value ^ value
        return hash_value

if __name__ == '__main__':
    #Time to test
    #Seed works
    hash = TabulationHash()
    hash_values = []
    for i in range(1000000):
        hash_values.append(hash(i))
    #print(hash_values)
    #Test uniformity of hash values
    #Hash values are Uniformly distributed! This is important for accuracy of hyperloglog to work
    plt.hist(hash_values, bins= 1000)
    plt.title("Distribution of hash values")
    plt.xlabel("Hash value")
    plt.ylabel("Frequency")
    plt.show()
