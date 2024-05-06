#!/usr/bin/env python3

from typing import List, Tuple
import pandas as pd # type: ignore
import argparse
import sys
from sklearn.metrics.pairwise import haversine_distances # type: ignore
from itertools import combinations
import numpy as np
from math import sin, cos, sqrt, asin
import numpy.typing as npt
import random
from operator import itemgetter
import time

# this should be replaced with the multiprocessing variant
#from queue import Queue
from multiprocessing import *
from multiprocessing import Array

def haversine(lat1: float, lon1: float, lat2: float, lon2: float)->float:
    """
    Computes haversine distance manually.
    
    Parameters:
    - lat1: latitude of point 1
    - lon1: longitude of point 1
    - lat2: latitude of point 2
    - lon2: longitude of point 2
    """
    return 2*asin(sqrt( sin((lat2-lat1)/2)**2 +
                            cos(lat1)*cos(lat2) * sin((lon2-lon1)/2)**2))


def find_nearest(X: npt.NDArray[np.float64], q: npt.NDArray)->int:
    """
    Find the index of the nearest point in X, with respect to a query point q.

    Parameters:
    - X: (n,2) dataset of (latitude,longitude) pairs
    - q: a (latitude,longitude) query point

    Return value:
    index i such that X[i,:] has minimal haversine distance wrt. q
    """
    D = haversine_distances(X,q.reshape(1,2))
    return int(np.argmin(D))



# TODO: change the type of A to be a multiprocessing array

def process(Q: Queue, R: Queue, A, n : int)->None:
    """
    Read one item at a time from the queue, until None is encountered,
    and query the array of latitude/longitude pairs for the nearest index

    Parameters:
    - Q: queue of (idx,latitude,longitude) pairs, until None is encountered
    - R: queue of (idx,i) pairs that contain the indices of nearest neighbors, 
         and ends with a None
    - A: an n*2 array of latitude longitude pairs
    """

    # TODO: change this to use np.frombuffer and get_obj() of the array to
    # create a shallow NumPy view into the underlying shared memory
    X: npt.NDArray[np.float64] = np.frombuffer(A.get_obj(), dtype=np.float64).reshape((n, 2))

    while True:
        q = Q.get()
        if q is None:
            break
        idx = q[0]
        q = np.array(q[1:])
        R.put((idx,find_nearest(X,q)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'Ufo',
        description = 'Use linear scan to detect the nearest UFO sighitings '
        'by the latitude and longitude, with respect to the haversine '
        'distance. Queries are read from stdin, one query per line, given '
        'in degrees.'
        )
    parser.add_argument('filename', type = str, default = 'ufo.csv',
                            help = 'database filename, should point to the '
                            '"ufo.csv" file',
                            nargs = '?')
    parser.add_argument('-w', '--workers', type = int, default = 1,
                            metavar = 'W',
                            help = 'Number of workers (processes)')

    args = parser.parse_args()

    start_time_sequential = time.time()
    # read data
    df = pd.read_csv(args.filename)
    n: int = df.shape[0]
    n_workers = args.workers
    locs: List[str] = df['location'].tolist()

    # TODO: add here memory allocation in the form of a multiprocessing array
    X_shared = Array('d', n * 2)

    # TODO: for easier processing, we create a NumPy array to access the
    # underlying memory; change this to point to the memory in the
    # multiprocessing array (using np.frombuffer)
    #X: npt.NDArray[np.float64] = np.zeros((n,2))

    X: npt.NDArray[np.float64] = np.frombuffer(X_shared.get_obj(), dtype=np.float64).reshape((n, 2))

    # convert to radians
    # note: Pandas stores data in Fortran order, we convert it to C order
    X[:,0] = df['latitude'] * (np.pi/180)
    X[:,1] = df['longitude'] * (np.pi/180)

    # this queue contains items to be consumed
    # TODO: change into multiprocessing queue ✅
    Q: Queue = Queue()

    # this queue contains the results
    # TODO: change into multiprocessing queue ✅
    R: Queue = Queue()

    # TODO: add creation of workers (processes) ✅
    processes = []
    for _ in range(n_workers):
        p = Process(target=process,args=(Q,R,X_shared,n))
        processes.append(p)

    # read input one line at a time from system input and enequeue them
    i = 0
    for line in sys.stdin:
        q: npt.NDArray[np.float64] = np.array(list(map(float,line.split()))) \
        * (np.pi/180)
        Q.put((i,q[0],q[1]))
        i += 1

    # TODO: change to work with multiple processes
    for _ in range(n_workers):
        Q.put(None)

    # TODO: this function should be executed in a different process ✅
    #process(Q,R,X_shared)

    # Assign target function and arguments ✅
    #for p in processes:
    #    p.target = process
    #    p.args = (Q,R,X_shared,n)

    start_time_parallel = time.time()

    # Start the processes ✅
    for p in processes:
        p.start()

    # TODO: add cleanup for processes ✅
    for p in processes:
        p.join()

    end_time_parallel = time.time()

    # read results from the result queue
    res: List[Tuple[int,int]] = list()
    for _ in range(i):
        r = R.get()
        res.append(r)

    # sort by the index so locations are printed in correct order
    res.sort()
    for (_,i) in res:
        print(locs[i])
    
    end_time_sequential = time.time()

    #time_parallel = end_time_parallel - start_time_parallel
    #time_sequential = end_time_sequential - start_time_sequential - time_parallel
    total_time = end_time_sequential - start_time_sequential
    print(total_time)


