 #!/usr/bin/env python3

import sys
from mrjob.job import MRJob,MRStep

class MRJobTwitterFollows(MRJob):
    # The final (key,value) pairs returned by the class should be
    # 
    # yield ('most followed id', ???)
    # yield ('most followed', ???)
    # yield ('average followed', ???)
    # yield ('count follows no-one', ???)
    #
    # You will, of course, need to replace ??? with a suitable expression
    def mapper(self,_,line):
        # Split the sentence into two parts based on the colon
        parts = line.split(':')
        # Extract the key and value
        key = parts[0].strip()
        values = parts[1].strip().split()
        # Return the key-value pair
        yield (key,len(values))

    def reducer(self,key,counts):
        yield (None,(key,sum(counts)))

    def reducer2(self,_,value):
        maximum = (None, -1)
        minimum = (None, float('inf'))
        total_users = 0
        total_following = 0
        no_following = 0
        for val in value:
            if (val[1]>maximum[1]):
                maximum = val
            if (val[1]<minimum[1]):
                minimum = val
            if (val[1]==0):
                no_following +=1
            total_following += val[1]
            total_users +=1
            
        yield ('most followed id', maximum[0])
        yield ('most followed', maximum[1])
        yield ('average followed', total_following/total_users)
        yield ('count follows no-one', no_following)

    def steps(self):
        return [MRStep(mapper = self.mapper, reducer = self.reducer),MRStep(reducer = self.reducer2)]

if __name__ == '__main__':
    MRJobTwitterFollows.run()

