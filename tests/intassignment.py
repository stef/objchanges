#!/usr/bin/env python3

from objchanges import diff, patch

old={'c': {'a': []}, '23': 'Oqu', '1': [[{}, {}], 5, {}, 42, []], 'a': 'cRL', '2': {}, '5': ['3yd', {}]}
oldpaths={('2', '5'), ('2', '3'), ('1', 1), ('1',), ('2',), ('1', 0, 1), ('1', 0, 1, 0), ('1', 0), ('1', 0, 2), ('1', 4), ('a',), ('1', 4, '2'), ('5', 0), ('1', 3), ('c',), ('5', 1), ('5',), ('1 ', 3, 'c'), ('1', 2), ()}
new={'c': {}, '1': [[42], [{}, {}, []], {}, {'2': 23, 'c': 'qvA'}, 42], '2': {'5': {}}, '5': ['3yd', []], '23': '8Vy', 'a': 42}
newpaths={('2', '5'), ('2', '3'), ('1', 1), ('1',), ('2',), ('1', 0, 1), ('1', 0, 1, 0), ('1', 0), ('1', 0, 2), ('1', 4), ('a',), ('1', 4, '2'), ('5', 0), ('1', 3), ('c',), ('5', 1), ('5',), ('1 ', 3, 'c'), ('1', 2), ()}
#diff=[{'type': 'added', 'data': {}, 'path': ['2', '5']}, {'type': 'added', 'data': [], 'path': ['5', 1]}, {'type': 'deleted', 'data': {}, 'path': ['5', 1]}, {'type': 'changed', 'data': ('Oqu', '8Vy'), 'path': ['23']}, {'type': 'deleted', 'data': [{}, {}], 'path': ['1', 0]}, {'type': 'added', 'data': 5, 'path': ['1', 1]}, {'type': 'added', 'data': [], 'path': ['1', 1, 2]}, {'type': 'added', 'data': [42], 'path': ['1', 0]}, {'type': 'added', 'data': {'2': 23, 'c': 'qvA'}, 'path': ['1', 3]}, {'type': 'deleted', 'data': 5, 'path': ['1', 1]}, {'type': 'deleted', 'data': [], 'path': ['1', 4]}, {'type': 'deleted', 'data': [], 'path': ['c', 'a']}, {'type': 'changed', 'data': ('cRL', 42), 'path': ['a']}]
# Traceback (most recent call last):
#   File "./fuzz.py", line 118, in <module>
#     assert diff(new, patch(old, d)) in [None, []]
#   File "/home/s/tasks/objchanges/objchanges.py", line 197, in patch
#     obj[change['path'][-1]]=deepcopy(change['data'])
# TypeError: 'int' object does not support item assignment

d = diff(old, new)
new2 = patch(old, d)
assert diff(new, new2) in [None, []]
