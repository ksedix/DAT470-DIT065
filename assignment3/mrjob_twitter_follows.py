 #!/usr/bin/env python3

from mrjob.job import MRJob

class MRJobTwitterFollows(MRJob):
    # The final (key,value) pairs returned by the class should be
    # 
    # yield ('most followed id', ???)
    # yield ('most followed', ???)
    # yield ('average followed', ???)
    # yield ('count follows no-one', ???)
    #
    # You will, of course, need to replace ??? with a suitable expression
    pass

if __name__ == '__main__':
    MRJobTwitterFollows.run()

