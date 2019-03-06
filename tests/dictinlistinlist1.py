#!/usr/bin/env python3
# throws
#Traceback (most recent call last):
#  File "./fuzz.py", line 98, in <module>
#    d = diff(old, new)
#  File "/home/s/tasks/objchanges/objchanges.py", line 42, in diff
#    r=diff(old.get(k),(new or {}).get(k), path+[k])
#  File "/home/s/tasks/objchanges/objchanges.py", line 42, in diff
#    r=diff(old.get(k),(new or {}).get(k), path+[k])
#  File "/home/s/tasks/objchanges/objchanges.py", line 47, in diff
#    return difflist(old, new, path)
#  File "/home/s/tasks/objchanges/objchanges.py", line 94, in difflist
#    newset,neworder=normalize_list(new)
#  File "/home/s/tasks/objchanges/objchanges.py", line 75, in normalize_list
#    objset.add(tuple(x))
#TypeError: unhashable type: 'dict'

from objchanges import diff, patch

def test(a, b):
    print("x"*80)
    #for i, x in enumerate(a): print("%2d" % i,sorted(x.items()))
    #print("")
    #for i, x in enumerate(b): print("%2d" % i,sorted(x.items()))
    d = diff(a,b)
    #print("")
    #for x in d: print(x)
    #print("")
    p = patch(a, d)
    assert p is not None
    tmp = diff(p,b)
    assert (tmp==None) or (len(tmp) == 0)
    if isinstance(tmp,list) and (len(tmp) != 0):
        print("patch(a, diff(a,b))!=b")
        for c in tmp:
            print(c)

old={'23': {'23': [[], {}], 'c': 'Jy9'}, '2': 1749, 'c': {}}
new={'23': {'23': [[{}], {}], 'c': 'Jy9'}, '2': 1749, 'c': {}}
#diff [{'type': 'added', 'data': (), 'path': ['23', '23', 0]}]
test(new,old)
