#!/usr/bin/env python3
from __future__ import annotations 
import argparse
import numpy as np
import numpy.typing as npt
from typing import Optional, Callable
from tabulation_hash import TabulationHash
import math
from multiprocessing import Pool

class HyperLogLog:
    #used for calculating hash on elements y
    _h: TabulationHash
    #Q: What is this used for?
    _f: Callable[[np.uint64],np.uint64]
    #used for storing m registers
    _M: npt.NDArray[np.uint8]
    #used for storing size of array. Has to be a power of 2.
    _m: int

    #p(x) takes a 32 bit unsigned int hash value and calculates the position of the leftmost 1-bit
    def p(self, x : np.uint32):
        if (x==0):
            #p(x) is not defined for x=0
            raise Exception
        else:
            for i in range(31,-1,-1):
                mask = (1 << i)
                if (x & mask):
                    return 32-i
    
    #why do we have x as a np.uint64 and why do we return a np.uint64 when the number is 10 bits?
    #I understand why we take np.uint64, but why do we return np.uint64 or does it not matter
    def multiply_shift_hash(self,x: np.uint64) -> np.uint64:
        a = np.uint64(0xc863b1e7d63f37a3)
        return (a*np.uint64(x)) >> np.uint64(64 - 10)


    def __init__(self, m: int, seed: Optional[int] = None):
        """
        Initialize a HyperLogLog sketch
        """
        self._m = m
        self._M = np.zeros(m, dtype=np.uint8)
        self._h = TabulationHash(seed)
        self._f = self.multiply_shift_hash

    def __call__(self, x: np.uint64):
        """
        Add element into the sketch
        """
        #trivial hashing index
        #index = x % self._m
        index = self._f(x) 
        hash_value = self._h(x)
        if self._M[index] == 0:
            self._M[index] = self.p(hash_value)
        else:
            self._M[index] = max(self._M[index],self.p(hash_value))

    def estimate(self)->float:
        """
        Return the present cardinality estimate
        """
        #constant for correcting the bias of the estimate
        a_m = 0.7213 / (1 + (1.079/self._m))

        right_sum = 0
        for i in range(self._m):
            right_sum += 1/(pow(2,self._M[i]))
        
        #the normalized harmonic mean
        normalized_harmonic_mean = a_m*pow(self._m,2)*(1/right_sum)

        return normalized_harmonic_mean

    def merge(self, other: HyperLogLog)->HyperLogLog:
        """
        Merge two sketches
        """
        merged_sketch = HyperLogLog(self._m)
        for i in range(self._m):
            merged_sketch[i] = max(self._M[i],other._M[i])
        return merged_sketch


def merge_hlls(hlls):
    merged_hll = hlls[0]
    for hll in hlls[1:]:
        merged_hll = merged_hll.merge(hll)
    return merged_hll

def process_chunk(chunk):
    hll = HyperLogLog(m)
    for i in chunk:
        hll(i)
    return hll

if __name__ == '__main__':
    #m = 1024, 2048, 4096
    parser = argparse.ArgumentParser(description='HyperLogLog Sketch')
    parser.add_argument('n', type=int, help='Number of unique values to feed into the sketch')
    parser.add_argument('m', type=int, help='Size of the sketch array (must be a power of 2)')
    parser.add_argument('-s', '--seed', type=int, help='Seed value for hash function (optional)')
    parser.add_argument('-w', '--workers', type=int, default=1, help='Number of workers for multiprocessing')
    args = parser.parse_args()

    m = args.m
    n = args.n
    seed = args.seed
    n_workers = args.workers

    hyper_log_log_sketch = HyperLogLog(m, seed)
    for i in range(1,n+1):
        hyper_log_log_sketch(i)
    print(hyper_log_log_sketch.estimate())

    #with Pool(processes=n_workers) as pool:
    #    hlls = pool.map(process_chunk, range(1,n+1),chunksize=n/n_workers)
    #Merge all HyperLogLog instances
    #final_hll = merge_hlls(hlls)
    #print(final_hll.estimate())








    

