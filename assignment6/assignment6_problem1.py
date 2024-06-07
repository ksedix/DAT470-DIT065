#!/usr/bin/env python3

import time
import argparse
import findspark
import numpy as np

from tabulation_hash import TabulationHash
findspark.init()
from pyspark import SparkContext

def multiply_shift_hash(x: np.uint64) -> np.uint64:
    a = np.uint64(0xc863b1e7d63f37a3)
    return (a*np.uint64(x)) >> np.uint64(64 - 10)

def p(x : np.uint32):
    if (x==0):
        raise Exception
    else:
        for i in range(31,-1,-1):
            mask = (1 << i)
            if (x & mask):
                return 32-i

def readLine(line):
    x,y = map(int,line.split())
    return [x,y]

def p(x : np.uint32):
    if (x==0):
        #p(x) is not defined for x=0
        raise Exception
    else:
        for i in range(31,-1,-1):
            mask = (1 << i)
            if (x & mask):
                return 32-i
            
def keyValue(x):
    random_arrays = broadcasted_random_arrays.value
    x = np.uint64(x)
    key = multiply_shift_hash(x)
    # Hash a 64-bit integer key x into 32-bit hash value
    bit_mask = np.uint64(0xffff)

    x_1 = x & bit_mask
    x_2 = (x >> np.uint64(16)) & bit_mask
    x_3 = (x >> np.uint64(32)) & bit_mask
    x_4 = (x >> np.uint64(48)) & bit_mask

    h_1 = random_arrays[0][x_1]
    h_2 = random_arrays[1][x_2]
    h_3 = random_arrays[2][x_3]
    h_4 = random_arrays[3][x_4]

    hash_x = np.uint32(h_1 ^ h_2 ^ h_3 ^ h_4)
    
    value = p(hash_x)
    return (key,value)

def multiply_shift_hash(x: np.uint64) -> np.uint64:
    a = np.uint64(0xc863b1e7d63f37a3)
    return (a*x) >> np.uint64(64 - 10)

def calculate_intermediate(tpl):
    return 1/(pow(2,tpl[1]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute Twitter followers.')
    parser.add_argument('-w','--num-workers',default=1,type=int,
                            help = 'Number of workers')
    parser.add_argument('-m',default=1024,type=int,
                            help = 'Size of Array')
    parser.add_argument('-s','--seed',default=None,type=int,
                            help = 'The random seed to use for Tabulation Hash')
    parser.add_argument('filename',type=str,help='Input filename')
    args = parser.parse_args()

    start = time.time()
    sc = SparkContext(master = f'local[{args.num_workers}]')

    m = args.m
    seed = args.seed
    tabulation_hash = TabulationHash(seed)

    broadcasted_random_arrays = sc.broadcast(tabulation_hash.random_arrays)

    lines = sc.textFile(args.filename)

    # fill in your code here
    twitter_ids = lines.flatMap(readLine)
    key_value_rdd = twitter_ids.map(keyValue)
    key_value_reduced = key_value_rdd.reduceByKey(lambda a,b : max(a,b))
    intermediate = key_value_reduced.map(calculate_intermediate)
    sum_intermediate = intermediate.reduce(lambda a,b : a+b)

    a_m = 0.7213 / (1 + (1.079/m))
    normalized_harmonic_mean = a_m*pow(m,2)*(1/sum_intermediate)
    
    end = time.time()
    
    total_time = end - start

    print(f'extimated number of users: {normalized_harmonic_mean}')
    print(f'num workers: {args.num_workers}')
    print(f'total time: {total_time}')

