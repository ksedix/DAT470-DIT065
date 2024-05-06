#!/usr/bin/env python3

import time
import argparse
import findspark
findspark.init()
from pyspark import SparkContext

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute Twitter followers.')
    parser.add_argument('-w','--num-workers',default=1,type=int,
                            help = 'Number of workers')
    parser.add_argument('filename',type=str,help='Input filename')
    args = parser.parse_args()

    start = time.time()
    sc = SparkContext(master = f'local[{args.num_workers}]')

    lines = sc.textFile(args.filename)

    # fill in your code here
    def readLine(line):
        parts = line.split(":")
        id = parts[0].strip()
        ids = parts[1].strip().split()
        return [(id,1) for id in ids] + [(id,0)]

    followers_tuples = lines.flatMap(readLine)
    #here, this was necessary, but was this necessary to do in pyspark_twitter_follows? 
    followers_sums = followers_tuples.reduceByKey(lambda a,b: a + b).cache()

    total_users = followers_sums.count()
    total_followers = followers_sums.values().sum()
    average_followers = total_followers / total_users

    no_followers_count = followers_sums.filter(lambda x : x[1]==0).count()

    most_followers_id = followers_sums.max(key = lambda x : x[1])[0]
    most_followers_count = followers_sums.values().max()
    
    end = time.time()
    
    total_time = end - start

    # the first ??? should be the twitter id
    print(f'max followers: {most_followers_id} has {most_followers_count} followers')
    print(f'followers on average: {average_followers}')
    print(f'number of user with no followers: {no_followers_count}')
    print(f'num workers: {args.num_workers}')
    print(f'total time: {total_time}')

