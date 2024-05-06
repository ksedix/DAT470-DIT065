 #!/usr/bin/env python3

from mrjob.job import MRJob

class MRJobTwitterFollowers(MRJob):
    # The final (key,value) pairs returned by the class should be
    # 
    # yield ('most followers id', ???)
    # yield ('most followers', ???)
    # yield ('average followers', ???)
    # yield ('count no followers', ???)
    #
    # You will, of course, need to replace ??? with a suitable expression
    pass

if __name__ == '__main__':
    MRJobTwitterFollowers.run()

