#!/usr/bin/env python3

import argparse
import numpy as np
from typing import Optional
import random
from matplotlib import pyplot as plt

class TabulationHash:

    def generate_random_bits(self,num_bits):
    # Generate a random integer with the specified number of bits
        return random.getrandbits(num_bits)

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the tabulation hash function.
        """
        if (seed is not None):
            random.seed(seed)
        self.random_arrays = [[self.generate_random_bits(32) for _ in range(pow(2,16))] for _ in range(4)]

    def __call__(self, x: np.uint64)->np.uint32:
        """
        Hash a 64-bit integer key x into 32-bit hash value
        """
        bit_mask = 0xffff
  
        x_1 = x & bit_mask
        #x_2 = np.right_shift(x,16) & bit_mask
        #x_3 = np.right_shift(x,32) & bit_mask
        #x_4 = np.right_shift(x,48) & bit_mask
        x_2 = (x >> 16) & bit_mask
        x_3 = (x >> 32) & bit_mask
        x_4 = (x >> 48) & bit_mask

        h_1 = self.random_arrays[0][x_1]
        h_2 = self.random_arrays[1][x_2]
        h_3 = self.random_arrays[2][x_3]
        h_4 = self.random_arrays[3][x_4]

        return (h_1 ^ h_2 ^ h_3 ^ h_4)

if __name__ == '__main__':
    pass
