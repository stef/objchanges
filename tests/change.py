#!/usr/bin/env python3
# throws

from objchanges import diff, patch

def test(a, b):
    print("x"*80)
    #print("a", a)
    #print("")
    #print("b", b)
    #print("")
    #print("_"*120)
    d = diff(a,b)
    #print("")
    #for x in sorted(d,key=lambda x: len(x['path'])): print(x)
    #print("")
    p = patch(a, d)
    assert p is not None
    tmp = diff(p,b)
    if len(tmp) != 0:
        print("_"*120)
        print("")
        print("patch(a, diff(a,b))!=b")
        print("b2", p)
        print("b ", b)
        print("diff")
        for x in sorted(tmp,key=lambda x: len(x['path'])): print(x)
    assert (tmp==[])

#diff [{'type': 'changed', 'path': ['b', 0], 'data': ([], {'2': []})}, {'type': 'changed', 'path': ['b', 1], 'data': ({'2': []}, [])}, {'type': 'added', 'path': ['b', 2, 0], 'data': [[[1749]]]}, {'type': 'added', 'path': ['b', 2, 1], 'data': [17, 1749, 'ZJQ', 23]}, {'type': 'added', 'path': ['b', 2, 2], 'data': 1749}, {'type': 'added', 'path': ['b', 2, 3], 'data': {'2': 42, 'a': 42, '5': {}, '23': {'23': 5, '2': {}, 'a': []}}}, {'type': 'added', 'path': ['b', 2, 4], 'data': 'kXd'}, {'type': 'deleted', 'path': ['b', 3, 0], 'data': [[[1749]]]}, {'type': 'added', 'path': ['b', 3, 1], 'data': [[[1749]]]}, {'type': 'changed', 'path': ['b', 3, 1], 'data': ([17, 1749, 'ZJQ', 23], '7oL')}, {'type': 'deleted', 'path': ['b', 3, 1], 'data': [17, 1749, 'ZJQ', 23]}, {'type': 'added', 'path': ['b', 3, 2], 'data': [17, 1749, 'ZJQ', 23]}, {'type': 'changed', 'path': ['b', 3, 2], 'data': (1749, '81m')}, {'type': 'added', 'path': ['b', 3, 0], 'data': [[]]}, {'type': 'added', 'path': ['b', 3, 3], 'data': 'RSV'}, {'type': 'added', 'path': ['b', 3, 4], 'data': 42}, {'type': 'added', 'path': ['b', 3, 5], 'data': []}, {'type': 'deleted', 'path': ['b', 3, 2], 'data': 1749}, {'type': 'deleted', 'path': ['b', 3, 3], 'data': {'2': 42, 'a': 42, '5': {}, '23': {'23': 5, '2': {}, 'a': []}}}, {'type': 'deleted', 'path': ['b', 3, 4], 'data': 'kXd'}, {'type': 'deleted', 'path': ['b', 4], 'data': [[[]], '7oL', '81m', 'RSV', 42, []]}]

#wtf change {'type': 'changed', 'path': ['b', 3, 1], 'data': ([17, 1749, 'ZJQ', 23], '7oL')} [[[]], [[[1749]]], [17, 1749, 'ZJQ', 23], 'RSV', 42, []]
#wtf change {'type': 'changed', 'path': ['b', 3, 2], 'data': (1749, '81m')} [[[]], [[[1749]]], [17, 1749, 'ZJQ', 23], 'RSV', 42, []]
#
#Traceback (most recent call last):
#  File "./fuzz.py", line 99, in <module>
#    assert diff(new, patch(old, d)) in [None, []]
#AssertionError

old={'b': [[], {'2': []}, [], [[[[1749]]], [17, 1749, 'ZJQ', 23], 1749, {'2': 42, 'a': 42, '5': {}, '23': {'23': 5, '2': {}, 'a': []}}, 'kXd'], [[[]], '7oL', '81m', 'RSV', 42, []]], '1': {}, 'c': 3}
new={'b': [{'2': []}, [], [[[[1749]]], [17, 1749, 'ZJQ', 23], 1749, {'2': 42, 'a': 42, '5': {}, '23': {'23': 5, '2': {}, 'a': []}}, 'kXd'], [[[]], '7oL', '81m', 'RSV', 42, []]], '1': {}, 'c': 3}
test(old,new)
