#!/usr/bin/env python3

from mrjob_twitter_follows import MRJobTwitterFollows
import time
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'mrjob_twitter_measure',
        description = 'Measure the running time of the twitter job',
        )
    parser.add_argument('-w', '--num-workers', type=int, default=1)
    parser.add_argument('filename')
    args = parser.parse_args()
    mr_job = MRJobTwitterFollows(args=[
        '-r', 'local',
        '--num-cores',
        str(args.num_workers),
        args.filename])
    
    start = time.time()
    with mr_job.make_runner() as runner:
        runner.run()
        for key, value in mr_job.parse_output(runner.cat_output()):
            print(key,value)
    end = time.time()
    print(f'Number of workers: {args.num_workers}')
    print(f'Time elapsed: {end-start} s')

    
