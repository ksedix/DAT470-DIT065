#!/usr/bin/env python3

import time
import argparse
import findspark
findspark.init()
from pyspark import SparkContext

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute Twitter follows.')
    parser.add_argument('-w','--num-workers',default=1,type=int,
                            help = 'Number of workers')
    parser.add_argument('filename',type=str,help='Input filename')
    args = parser.parse_args()

    start = time.time()
    sc = SparkContext(master = f'local[{args.num_workers}]')

    lines = sc.textFile(args.filename)

    # fill in your code here
    raise NotImplementedError()
    
    end = time.time()
    
    total_time = end - start

    # the first ??? should be the twitter id
    print(f'max follows: ??? follows ???')
    print(f'users follow on average: ???')
    print(f'number of user who follow no-one: ???')
    print(f'num workers: {args.num_workers}')
    print(f'total time: {total_time}')

