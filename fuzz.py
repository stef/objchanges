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

def del_path(paths, path):
    if path == tuple(): return set()
    for p in list(paths):
        if p[:len(path)]==path: paths.remove(p)
    return paths

def mutate(old, paths):
    for _ in range(choice((1,5,20))):
        while True:
            new, paths= evolve(old, paths)
            if old != new: return new, paths

def evolve(old, paths):
    obj = deepcopy(old)
    # chose which item to change
    done = False
    while not done:
        path = choice(tuple(paths))
        item = getitem(obj, path)
        operation = choice(('add', 'del'))
        if operation == 'add':
            if isinstance(item, dict):
                tmp = list(dict_keys - set(item.keys()))
                if not tmp: continue
                k = choice(tmp)
                item[k]=rnd_obj()
                paths.add(path + tuple([k]))
                done = True
            elif isinstance(item,list):
                if len(item)>5: continue
                item.insert(randrange(len(item)+1), rnd_obj())
                paths.add(path + tuple([len(item)-1]))
                done = True
        elif operation == 'del':
            if isinstance(item, dict):
                if not item: continue
                k = choice(tuple(item.keys()))
                del item[k]
                paths=del_path(paths,path + tuple(k,))
                done=True
            elif isinstance(item,list):
                if len(item) == 0: continue
                i = randrange(len(item))
                del item[i]
                paths=del_path(paths,path + tuple([len(item)]))
                done=True
    return obj, paths

old={}
oldpaths=set([tuple(),])
i = 0
while True:
    print("\r%d" % i, end='')
    #print(old)
    #print(oldpaths)
    new, newpaths = mutate(old,oldpaths)
    try:
        d = diff(old, new)
        assert diff(new, patch(old, d)) in [None, []]
    except:
        print("\nfail:\nold {!r}\nold paths{!r}\nnew {!r}\nnewpaths {!r}\ndiff {!r}".format(old,oldpaths,new,newpaths,d))
        raise
        traceback.print_exc()
    old = new
    oldpaths = newpaths
    i += 1
