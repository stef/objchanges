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
    for p in list(paths):
        if p[:len(path)]==path: paths.remove(p)
    return paths

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
                paths.add(tuple(path + tuple(k,)))
                done = True
            elif isinstance(item,list):
                if len(item)>5: continue
                item.insert(randrange(len(item)+1), rnd_obj())
                paths.add(tuple(path + tuple([len(item)-1])))
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
        #else: # operation == "change"
        #    if isinstance(item, dict):
        #        if not item: continue
        #        if choice(('k','v')) == 'k':
        #            #change key
        #            tmp = list(dict_keys - set(item.keys()))
        #            if not tmp: continue
        #            ok = choice(tuple(item.keys()))
        #            nk = choice(tmp)
        #            item[nk] = item[ok]
        #            del item[ok]
        #            paths.remove(tuple(path + tuple(ok,)))
        #            paths.add(tuple(path + tuple(nk,)))
        #            # todo rename all paths ok -> nk
        #            done=True
        #        else:
        #            # change value
        #            k = choice(tuple(item.keys()))
        #            item[k]=rnd_obj()
        #            done=True
        #    elif isinstance(item, list):
        #        if not item: continue
        #        i = randrange(len(item)+1)
        #        item[i]=rnd_obj()
        #        # todo remove paths that were belonging to the changed item if it is a dict/list
    return obj, paths

old={}
paths=set([tuple(),])
print(old)
print(paths)
while True:
    new, paths = evolve(old,paths)
    print(new)
    print(paths)
    assert diff(new, patch(old, diff(old, new))) in [None, []]
    old = new
