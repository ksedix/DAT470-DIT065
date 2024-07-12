import argparse
import math
import multiprocessing
import time
import numpy as np
from hyperloglog import process_batch

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Hyperloglog cardinality estimation algorithm")
    parser.add_argument("n",type=int,help="Number of unique items to feed to the sketch")
    parser.add_argument("-m","--size",type=int,default=1024,help="Size of the hyperloglog sketch, must be a power of 2(Deafult 1024)")
    parser.add_argument("-w","--workers",type=int,default=1,help="Number of workers/CPU cores to process the data")
    parser.add_argument("-s","--seed",type=int,default=None,help="The PRNG seed used for creating the sketch including the tabulation hash")

    args = parser.parse_args()
    n = args.n
    m = args.size
    #do not use more workers than there are CPU cores in your system
    #this will only throttle the performance and will not benefit
    #parallelization.
    n_workers = args.workers
    
    start = time.time()
    batch_size = math.ceil(n/n_workers)
    #We will not create the batches using a generator expression here
    #The reason is that we will need to use them over and over for multiple
    #iterations
    batches = [(i,i+batch_size,m) for i in range(0,n,batch_size)]

    list_of_sketches = []

    # run the code in hyperloglog.py 100 times and collect the summary statistics
    for i in range(100):
        with multiprocessing.Pool(processes=n_workers) as pool:
            sketches = pool.map(process_batch,batches)
            list_of_sketches.append(sketches)
    merged_sketches = []
    #mergin
    merge_start = time.time()
    for sketches in list_of_sketches:
        merged_sketch = sketches[0]
        for sketch in sketches[1:]:
            merged_sketch = merged_sketch.merge(sketch)
        merged_sketches.append(merged_sketch)
    end = time.time()

    estimates = [merged_sketch.estimate() for merged_sketch in merged_sketches]
    average_estimate = np.average(estimates)
    #calculate the percentage of estimates that are within 10% error margin from the real cardinality/value. Multiply by 100 to get percentage
    ten_percent_estimates = 100* len([estimate for estimate in estimates if estimate>=0.9*n and estimate<=1.1*n]) / len(estimates)
    print(estimates)
    print(f'The average estimate was {average_estimate}')
    print(f'The fraction of estimates within 10% of the real cardinality was {ten_percent_estimates}')
    #Parallelization works and makes the program faster!
    print(f'The total running time of the program was {end-start} seconds')
    print(f'The running time of merge operation is {end-merge_start} seconds')