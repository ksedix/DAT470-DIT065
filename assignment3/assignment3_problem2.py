 #!/usr/bin/env python3

from mrjob.job import MRJob,MRStep

class MRJobTwitterFollowers(MRJob):
    # The final (key,value) pairs returned by the class should be
    # 
    # yield ('most followers id', ???)
    # yield ('most followers', ???)
    # yield ('average followers', ???)
    # yield ('count no followers', ???)
    #
    # You will, of course, need to replace ??? with a suitable expression
    def mapper(self,_,input):
        parts = input.split(':')
        user_id = parts[0].strip()
        ids = parts[1].strip().split()
        yield (user_id,0)
        for id in ids:
            yield (id,1)

    def reducer(self,id,ones):
        value = (id,sum(ones))
        yield (None,value)

    def reducer2(self,_,values):
        maximum = (None, -1)
        minimum = (None, float("inf"))
        no_followers = 0
        total_followers = 0
        total_accounts = 0
        for value in values:
            if (value[1]>maximum[1]):
                maximum = value
            if (value[1]<minimum[1]):
                minimum = value
            if (value[1]==0):
                no_followers +=1
            total_followers += value[1]
            total_accounts +=1

        yield ('most followers id', maximum[0])
        yield ('most followers', maximum[1])
        yield ('average followers', total_followers/total_accounts)
        yield ('count no followers', no_followers)

    def steps(self):
        return [MRStep(mapper = self.mapper, reducer = self.reducer), MRStep(reducer = self.reducer2)]

if __name__ == '__main__':
    MRJobTwitterFollowers.run()

