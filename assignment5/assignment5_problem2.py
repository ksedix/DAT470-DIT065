#!/usr/bin/env python3
import argparse
import math
import multiprocessing
import time
import numpy as np
import numpy.typing as npt
from typing import Optional, Callable
from tabulation_hash import TabulationHash

class HyperLogLog:
    #Tabulation hash used to generate hash values
    _h: TabulationHash
    #Another hash function used to generate a hash value which is a random index in the array _M
    _f: Callable[[np.uint64],np.uint64]
    #Array of m registers which store the values added to the sketch
    _M: npt.NDArray[np.uint8]
    #Size of M array
    _m: int

    def multiply_shift_hash(self, x : np.uint64):
        a = np.uint64(0xc863b1e7d63f37a3)
        #L should be equal to the number of bits required to represent the size of the array M
        #For example if M has size 1024, we require 10 bits to represent all the indices from 0-1023
        l = math.log2(self._m)
        return (a*x) >> np.uint(64-l)
    
    #Calculate the position of the leftmost 1 bit in a 32 bit hash value
    def p(self, x:np.uint32):
        bit_mask = np.uint32(1)
        for i in range(31,-1,-1):
            if x & (bit_mask << i):
                #return the position of the leftmost 1-bit. This will be 1 if the position of 
                #the leftmost 1 bit is the 32th bit, and 32 if it is the 1st bit
                return 32-i
        #if the value has no leftmost 1 bit, return 0
        return 0
    
    def __init__(self, m: int, seed: Optional[int] = None, tabulation_hash : TabulationHash = None):
        """
        Initialize a HyperLogLog sketch
        """
        self._M = np.zeros(m, dtype=np.uint8)
        self._m = m
        if tabulation_hash == None:
            self._h = TabulationHash(seed)
        else:
            #Don't recompute tabulation hash if one is already given
            self._h = tabulation_hash
        self._f = self.multiply_shift_hash

    def __call__(self, x: np.uint64):
        """
        Add element into the sketch
        """
        #There are 4 steps when adding element to sketch.
        #1. Use the tabulation hash to hash the element 
        #2. Calculate the position of the leftmost 1 bit in the hash value
        #3. Use the multiply-shift hash to hash the element to get random index
        #4. Store the position of the leftmost 1 bit in the random index

        #Turn x into a 64 bit unsigned numpy integer explicitly
        x = np.uint64(x)

        hash = self._h(x)
        leftmost_1_bit = self.p(hash)
        random_index = self.multiply_shift_hash(x)
        self._M[random_index] = max(self._M[random_index],leftmost_1_bit)

    def estimate(self)->float:
        """
        Return the present cardinality estimate
        """
        a_m = 0.7213 / (1 + 1.079/self._m)
        normalized_harmonic_mean = a_m*self._m**2*1/sum([1/2**self._M[i] for i in range(self._m)])
        return normalized_harmonic_mean

    def merge(self, other: 'HyperLogLog')->'HyperLogLog':
        """
        Merge two sketches
        """
        merged_sketch = HyperLogLog(self._m,tabulation_hash=self._h)
        #The value in the registers of the merged sketch should be the 
        #elementwise maximum between the corresponding values of the 2 subsketches
        merged_sketch._M = np.maximum(self._M,other._M)
        return merged_sketch


#Create process batch function that will be used by each worker/cpu core to process each batch
def process_batch(batch):
    start, end, m = batch
    sketch = HyperLogLog(m)
    for i in range(start,end):
        sketch(i)
    return sketch

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Hyperloglog cardinality estimation algorithm")
    parser.add_argument("n",type=int,help="Number of unique items to feed to the sketch")
    parser.add_argument("-m","--size",type=int,default=1024,help="Size of the hyperloglog sketch, must be a power of 2(Deafult 1024)")
    parser.add_argument("-w","--workers",type=int,default=1,help="Number of workers/CPU cores to process the data")
    parser.add_argument("-s","--seed",type=int,default=None,help="The PRNG seed used for creating the sketch including the tabulation hash")

    args = parser.parse_args()
    n = args.n
    m = args.size
    n_workers = args.workers
    
    start = time.time()
    batch_size = math.ceil(n/n_workers)
    #Create the batches using a generator expression to save memory. This can not be done in the experimental part
    batches = ((i,i+batch_size,m) for i in range(0,n,batch_size))

    with multiprocessing.Pool(processes=n_workers) as pool:
        sketches = pool.map(process_batch,batches)
    #Merging is inefficient. We can make it faster
    merge_start = time.time()
    merged_sketch = sketches[0]
    for sketch in sketches[1:]:
        merged_sketch = merged_sketch.merge(sketch)
    
    end = time.time()

    print(merged_sketch.estimate())
    #Parallelization works and makes the program faster!
    print(f'The total running time of the program was {end-start} seconds')
    print(f'The running time of merge operation is {end-merge_start} seconds')