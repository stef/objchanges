#!/usr/bin/env python3
# throws
#['ezw', []]
#Traceback (most recent call last):
#  File "./fuzz.py", line 103, in <module>
#    assert diff(new, patch(old, diff(old, new))) in [None, []]
#  File "/home/s/tasks/objchanges/objchanges.py", line 42, in diff
#    r=diff(old.get(k),(new or {}).get(k), path+[k])
#  File "/home/s/tasks/objchanges/objchanges.py", line 47, in diff
#    return difflist(old, new, path)
#  File "/home/s/tasks/objchanges/objchanges.py", line 93, in difflist
#    oldset,oldorder=normalize_list(old)
#  File "/home/s/tasks/objchanges/objchanges.py", line 75, in normalize_list
#    objset.add(tuple(x))
#TypeError: unhashable type: 'dict'

from objchanges import diff, patch, revert

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
    p = revert(b, d)
    assert p is not None
    tmp = diff(p,a)
    if len(tmp) != 0:
        print("_"*120)
        print("revert(b, diff(a,b))!=a")
        print("a2", p)
        print("diff")
        for x in sorted(tmp,key=lambda x: len(x['path'])): print(x)
    assert (tmp==[])

old={'a': [{'5': {'1': 3}, '2': {'2': 'sZ5'}}, ['ezw']], '1': 23, 'c': 'm0L'}
oldpaths={('a', 1, 0), ('c',), ('a', 1), ('a', 0), ('a', 0, '2'), ('a',), ('a', 0, '5'), (), ('a', 0, '5', '1'), ('1',), ('a', 0, '2', '2')}
new={'a': [{'5': {'1': 3}, '2': {'2': 'sZ5'}}, ['ezw', []]], '1': 23, 'c': 'm0L'}
newpaths={('a', 1, 0), ('c',), ('a', 1), ('a', 0), ('a', 0, '2'), ('a', 1, 1), ('a',), ('a', 0, '5'), (), ('a', 0, '5', '1'), ('1',), ('a', 0, '2', '2')}
test(new,old)
