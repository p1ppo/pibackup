import os
import sys
import pprint

HOME = ".\\"
PATH = ".\\backup\\"

os.curdir

walk_path = os.path.join(HOME, PATH)

try:
    walk = os.walk(walk_path)
    file_list = walk.__next__()[2]
    print(file_list)
except StopIteration:
    os.mkdir(walk_path)
except:
    print("Other issue")
    raise
