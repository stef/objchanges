#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#    This file is part of objchanges

#    objchanges is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    objchanges is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with objchanges  If not, see <http://www.gnu.org/licenses/>.

# 2019 (C) Stefan Marsiske <7o5rfu92t@ctrlc.hu>

import string
from copy import deepcopy
from random import choice, choices, randrange
from objchanges import getitem, diff, patch

dict_keys = {'a', 'b', 'c', '5', '1', '2', '23'}

def rnd_str(size=3):
    return ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=size))

def rnd_obj():
    return choice(({},[],choice((5,23,42,3,17,1749)), rnd_str()))

def mutate(old):
    for _ in range(choice((1,5,20))):
        while True:
            new = evolve(old)
            if old != new: return new

def getpaths(obj):
    res = [tuple()]
    res.extend(_getpaths(obj, tuple()))
    return tuple(res)

def _getpaths(obj, path):
    res = []
    if hasattr(obj,'keys'):
        for k in obj.keys():
            res.append(path + tuple([k]))
            tmp = _getpaths(obj[k], path + tuple([k]))
            if tmp: res.extend(x for x in tmp if x)
        return tuple(res)
    elif hasattr(obj,'__iter__') and not isinstance(obj,str):
        for k in range(len(obj)):
            res.append(path + tuple([k]))
            tmp = _getpaths(obj[k], path + tuple([k]))
            if tmp: res.extend(x for x in tmp if x)
        return res

def evolve(old):
    obj = deepcopy(old)
    # chose which item to change
    done = False
    while not done:
        path = choice(getpaths(obj))
        item = getitem(obj, path)
        operation = choice(('add', 'del'))
        if operation == 'add':
            if isinstance(item, dict):
                tmp = list(dict_keys - set(item.keys()))
                if not tmp: continue
                k = choice(tmp)
                item[k]=rnd_obj()
                done = True
            elif isinstance(item,list):
                if len(item)>5: continue
                item.insert(randrange(len(item)) if len(item) else 0, rnd_obj())
                done = True
        elif operation == 'del':
            if isinstance(item, dict):
                if not item: continue
                k = choice(tuple(item.keys()))
                del item[k]
                done=True
            elif isinstance(item,list):
                if len(item) == 0: continue
                i = randrange(len(item))
                del item[i]
                done=True
    return obj

old={}
i = 0
while True:
    print("\r%d" % i, end='')
    #print(old)
    new = mutate(old)
    try:
        d = diff(old, new)
        assert diff(new, patch(old, d)) in [None, []]
    except:
        print("\nfail:\nold {!r}\nnew {!r}\ndiff {!r}".format(old,new,d))
        raise
        traceback.print_exc()
    old = new
    i += 1
