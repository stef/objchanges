#!/usr/bin/env python3
from objchanges import diff, patch

old={'a': {'c': {'1': 23}, 'b': 'OAO'}, 'c': [[17]]}
oldpaths={('b', '2', '3'), ('c', 2), ('c',), ('c', 0), ('2',), (), ('b', '2'), ('c', 1), ('b',), ('2', '3')}
new= {'c': [{}, {}, {}], '23': 5, 'b': {'2': 'bi9', '23': []}, '2': 23}
newpaths= {('b', '2', '3'), ('c', 2), ('c',), ('c', 0), ('2',), (), ('b', '2'), ('c', 1), ('b',), ('2', '3')}

d = diff(old, new)
new2 = patch(old, d)
assert diff(new, new2) in [None, []]
