#!/usr/bin/env python3

import numpy as np
from typing import Optional

class TabulationHash:
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the tabulation hash function.
        """
        raise NotImplementedError()

    def __call__(self, x: np.uint64)->np.uint32:
        """
        Hash a 64-bit integer key x into 32-bit hash value
        """
        raise NotImplementedError()

if __name__ == '__main__':
    pass
