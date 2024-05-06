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

    def readLine(line):
        parts = line.split(":")
        id = parts[0].strip()
        ids = parts[1].strip().split()
        return (id,len(ids))

    # fill in your code here
    following_tuples = lines.map(readLine)
    #Q: Is this necessary?
    following_sums = following_tuples.reduceByKey(lambda a,b : a+b).cache()
    
    #Number of unique users
    count_users = following_sums.count()
    #Total number of followings from all users combined
    total_followings = following_sums.values().sum()
    #Average number of followings
    average_followings = total_followings / count_users
    #the id of the user that follows the most accounts
    most_followings_id = following_sums.max(key = lambda x:x[1])[0]
    #Number of accounts followed by the user that follows the most accounts
    maximum_followings = following_sums.values().max()

    # the number of accounts with zero followings, i.e. who follow no one 
    count_zero_followings = following_sums.filter(lambda x: x[1]==0).count()

    end = time.time()
    
    total_time = end - start

    # the first ??? should be the twitter id
    print(f'max follows: {most_followings_id} follows {maximum_followings}')
    print(f'users follow on average: {average_followings}')
    print(f'number of user who follow no-one: {count_zero_followings}')
    print(f'num workers: {args.num_workers}')
    print(f'total time: {total_time}')

