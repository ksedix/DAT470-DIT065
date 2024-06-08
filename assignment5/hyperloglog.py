#!/usr/bin/env python3

import numpy as np
import numpy.typing as npt
from typing import Optional, Callable
from problem1 import TabulationHash

class HyperLogLog:
    _h: TabulationHash
    _f: Callable[[np.uint64],np.uint64]
    _M: npt.NDArray[np.uint8]
    
    def __init__(self, m: int, seed: Optional[int] = None):
        """
        Initialize a HyperLogLog sketch
        """
        self._M = np.zeros(m, dtype=np.uint8)
        raise NotImplementedError()

    def __call__(self, x: np.uint64):
        """
        Add element into the sketch
        """
        raise NotImplementedError()

    def estimate(self)->float:
        """
        Return the present cardinality estimate
        """
        raise NotImplementedError()

    def merge(self, other: HyperLogLog)->HyperLogLog:
        """
        Merge two sketches
        """
        raise NotImplementedError()

if __name__ == '__main__':
    pass
