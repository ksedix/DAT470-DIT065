#!/usr/bin/env python3

import argparse
import math
import multiprocessing
import time
import numpy as np
import numpy.typing as npt
from typing import Optional, Callable
from tabulation_hash import TabulationHash


#Q: Why do we hash value before we calculate the position of the leftmost 1 bit? What would happen if we did not do it?
#Q: 𝑚loglog𝑛 = 1024⋅5 where did the value 5 come from? Slide 47
#Q: why is signature of f function [[np.uint64],np.uint64]. It takes a 64 bit number but returns a 10 bit value
#Q: how to limit bit length of multiplyshift function? When you multiply a with x the result can have more than 64 bits, 
#so you can't shift it by just 54 bits. You have to shift it by 55 bits in that case. But your c function in the slides 17 lecture9.pdf does not do this.
#is it because C automatically crops the result to 64 bits if you multiply 2 64 bits values or is the example incomplete as well?
#Q: When calculating position of leftmost 1-bit in hash value using p function, do you have to handle the case when the value is 0, i.e. has no leftmost 1-bit?
#or should that case never occur?
#Q: How to implement multiprocessing on hyperloglog.

class HyperLogLog:
    _h: TabulationHash
    _f: Callable[[np.uint64],np.uint64]
    _M: npt.NDArray[np.uint8]
    _m: np.uint64

    def multiply_shift_hash(self, x:np.uint64) -> np.uint64:
        a = np.uint64(0xc863b1e7d63f37a3)
        #overflow will occur here
        result = a*x
        #shift amount must be a numpy int
        return result >> np.uint64(64-10)
    
    #takes a 32 bit hash value and returns the position of the leftmost 1, which can be at most 32. So it can be represented with 8 bits
    def p(self, x:np.uint32) -> np.uint8:
        bit_mask = np.uint32(1)
        for i in range(1,33):
            if (x & (bit_mask<<np.uint8(32-i))):
                return i
        return 0

    
    def __init__(self, m: int, seed: Optional[int] = None):
        """
        Initialize a HyperLogLog sketch
        """
        self._M = np.zeros(m, dtype=np.uint8)
        self._m = m
        self._f = self.multiply_shift_hash
        self._h = TabulationHash(seed)

    def __call__(self, x: np.uint64):
        """
        Add element into the sketch
        """
        x = np.uint64(x)
        #calculate the index of the register to store the value in.
        index = self._f(x)
        #apply hash function to the value.
        hash_value = self._h(x)
        #calculate the position of the leftmost 1 bit in the hash value and put it in the register if it is larger than previously stored value
        self._M[index] = max(self._M[index], self.p(hash_value))

    def estimate(self)->float:
        """
        Return the present cardinality estimate
        """
        a_m = 0.7213 / (1+(1.079/self._m))
        return a_m*self._m**2*(1/sum([1/2**self._M[i] for i in range(self._m)]))


    def merge(self, other: 'HyperLogLog')->'HyperLogLog':
        """
        Merge two sketches
        """
        merged_sketch = HyperLogLog(self._m)
        for i in range(self._m):
            merged_sketch._M[i] = max(self._M[i],other._M[i])
        return merged_sketch


def worker_function(batch):
    """Function to be executed by each worker process."""
    sketch = HyperLogLog(1024)
    for i in range(batch[0],batch[1]):
        sketch(i)
    return sketch


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HyperLogLog algorithm for estimating cardinality")
    parser.add_argument('-w','--workers', type=int, help='The number of workers', default=1)
    parser.add_argument('n',type=int, help='The number of unique values to feed into the sketch')

    args = parser.parse_args()

    w = args.workers
    n = args.n
    batch_size = math.ceil(n / w)
    batches = [(i,min(i+batch_size,n)) for i in range(0,n,batch_size)]

    start = time.time()

    with multiprocessing.Pool(processes=w) as pool:
        results = pool.map(worker_function,batches)

    if results:
        merged_sketch = results[0]
        for sketch in results[1:]:
            merged_sketch = merged_sketch.merge(sketch)
    
    end = time.time()

    print(merged_sketch.estimate())
    print(f'It took {end-start} seconds')
    print(f'Number of workers: {w}')




