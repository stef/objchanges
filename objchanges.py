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

from operator import itemgetter
from copy import deepcopy
import functools

def diff(old,new):
    o = normalize(deepcopy(old))
    n = normalize(deepcopy(new))
    return _diff(o, n, old, new)

def _diff(old, new, o, n, opath=[], npath=[]):
    if old==None and new!=None:
        return [{'type': 'added', 'path': npath, 'data': getitem(n,npath)}]
    if new==None and old!=None:
        return [{'type': 'deleted', 'path': opath, 'data': getitem(o,opath)}]
    if not type(old)==type(new):
        return [{'type': 'changed', 'path': npath, 'data': (getitem(o,opath), getitem(n,npath))}]
    if hasattr(old,'keys'):
        res=[]
        for k in set(list(old.keys()) + list((new or {}).keys())):
            r=_diff(old.get(k),(new or {}).get(k), o, n, opath+[k], npath+[k])
            res.extend(r)
        return res
    if hasattr(old,'__iter__') and not isinstance(old,str):
        return difflist(old, new, o, n, opath, npath)
    if (([type(x) for x in [old, new]] == [ str, str ] and
           ''.join(old.split()).lower() != ''.join(new.split()).lower()) or
          old != new):
        return [{'type': u'changed', 'path': npath, 'data': (getitem(o,opath), getitem(n,npath))}]
    return []

def isprefix(a, b):
    if len(b) < len(a):
        return False
    return all(a[i] == b[i] for i in range(len(a)))

def difflist(old, new, o, n, opath, npath):
    oldset,oldorder=normalize_list(old)
    newset,neworder=normalize_list(new)
    if len(oldset) != len(old) or len(newset) != len(new):
        # we have duplicate elements in the list, fallback to naive difflist
        return naive_difflist(old, new, o, n, opath, npath)

    oldunique=sorted(oldset - newset, key=lambda x: oldorder[x])
    newunique=sorted(newset - oldset, key=lambda x: neworder[x])

    # check if all-atomic list
    if any(type(x) not in (dict, list, tuple, hashabledict) for x in oldunique+newunique):
        return atomiclistdiff(o, oldset, oldorder, oldunique, n, newset, neworder, newunique, opath, npath)

    # all the same
    if not (oldunique or newunique): return []
    #import code; code.interact(local=locals());
    ret=[]
    for oe in list(oldunique):
        candidates=sorted([(oe, ne,
                            _diff(oe, ne, o, n,
                                  opath + [oldorder[oe]],
                                  npath + [neworder[ne]]))
                            for ne in list(newunique)],
                           key=lambda a: len(a[2]))
        # find deep matches first
        if len(candidates) and (len(candidates[0][2])*3<=(len(candidates[0][1]) if isinstance(candidates[0][1], tuple) else 3)):
            if oldorder[oe] != neworder[candidates[0][1]]:
                oldobj = getitem(o, opath + [oldorder[oe]])
                patches = []
                for p in candidates[0][2]:
                    nopath = (opath+[oldorder[oe]])
                    if isprefix(nopath,p['path']) and nopath!=p['path']:
                        tmp=deepcopy(p)
                        tmp['path']=p['path'][len(nopath):]
                        patches.append(tmp)
                oldobj=patch(oldobj, patches)
                ret.append({'type': u'deleted', 'path': opath + [oldorder[oe]], 'data': oldobj})
                ret.append({'type': u'added', 'path': npath + [neworder[candidates[0][1]]], 'data': oldobj})
            ret.extend(candidates[0][2])
            oldunique.remove(candidates[0][0])
            newunique.remove(candidates[0][1])
    # handle added
    if newunique:
        ret.extend(sorted([{'type': u'added', 'path': npath + [neworder[e]], 'data': getitem(n,npath + [neworder[e]])} for e in newunique], key=itemgetter('path')))
    # handle deleted
    if oldunique:
        ret.extend(sorted([{'type': u'deleted', 'path': opath + [oldorder[e]], 'data': getitem(o,opath + [oldorder[e]])} for e in oldunique], key=itemgetter('path')))
    no = sorted([(neworder[common], common) for common in oldset & newset])
    oo = sorted([(oldorder[common], common) for common in oldset & newset])
    for (ni, ne), (oi, oe) in zip(no,oo):
        if ne == oe: continue
        ret.append({'type': u'changed', 'path': npath + [ni], 'data': (oe, ne)})
    return ret

def naive_difflist(old, new, o, n, opath, npath):
    # we have duplicate elements in the list, fallback to naive difflist
    os = len(old)
    ns = len(new)
    ret = []
    if os>ns:
        for i, (oe, ne) in enumerate(zip(old[:ns],new)):
            ret.extend(_diff(oe,ne,o,n,opath + [i],npath + [i]))
        ret.extend(sorted([{'type': u'deleted',
                            'path': opath + [ns+i],
                            'data': getitem(o,opath + [ns+i])}
                           for i in range(os - ns)], key=itemgetter('path')))
    elif ns>os:
        for i, (oe, ne) in enumerate(zip(old,new[:os])):
            ret.extend(_diff(oe,ne,o,n,opath + [i],npath + [i]))
        ret.extend(sorted([{'type': u'added',
                            'path': npath + [os+i],
                            'data': getitem(n,npath + [os+i])}
                           for i in range(ns - os)], key=itemgetter('path')))
    else:
        for i, (oe, ne) in enumerate(zip(old,new)):
            ret.extend(_diff(oe,ne,o,n,opath + [i],npath + [i]))
    return ret

def atomiclistdiff(o, oldset, oldorder, deleted, n, newset, neworder, added, opath, npath):
    # todo test reordering atoms that are shared between old and new
    ret = []
    if added:
        ret.extend(sorted([{'type': u'added', 'path': npath + [neworder[e]], 'data': getitem(n,npath + [neworder[e]])} for e in added], key=itemgetter('path')))
    # handle deleted
    if deleted:
        ret.extend(sorted([{'type': u'deleted', 'path': opath + [oldorder[e]], 'data': getitem(o,opath + [oldorder[e]])} for e in deleted], key=itemgetter('path')))
    no = sorted([(neworder[common], common) for common in oldset & newset])
    oo = sorted([(oldorder[common], common) for common in oldset & newset])
    for (ni, ne), (oi, oe) in zip(no,oo):
        if ne == oe: continue
        ret.append({'type': u'changed', 'path': npath + [ni], 'data': (oe, ne)})
    return ret

class hashabledict(dict):
    val = None
    def __hash__(self):
        if not self.val:
            self.val=hash(str(sorted(self.items())))
        return self.val

def normalize(obj):
    if isinstance(obj,bytes):
        return obj.decode('utf-8')
    if isinstance(obj,str):
        return obj
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    if isinstance(obj,dict):
        return hashabledict({k:normalize(v) for k,v in obj.items()})
    if hasattr(obj, '__iter__'):
        return tuple(normalize(e) for e in obj)
    return obj

def normalize_list(obj):
    if not obj: return set(), {}
    objset=set(obj) # duplicates will be ignored
    objorder={e: i for i, e in enumerate(obj)} # the last duplicates position will overwrite previous positions
    return objset, objorder

#### patch stuff starts here ####

def getitem(item,path):
    if item in ({},[],tuple()) or path in ([],tuple()): return item
    if isinstance(item,dict) and path[0] not in item:
        return None
    try:
        return getitem(item[path[0]], path[1:])
    except:
        return None

def sortpaths(a,b):
    # should give this output ['activities', 0, 'docs', 0], ['activities', 0, 'docs', 1, 'url']
    # now gives the reverse
    a=a['path']
    b=b['path']
    if a[:len(b)] == b:
        # b is prefix of a
        return 1
    if b[:len(a)] == a:
        # a is prefix of b
        return -1
    if a>b: return -1
    if a<b: return 1
    return 0

def patch(obj, changes):
    res = deepcopy(obj)
    for l in sorted({len(x['path']) for x in changes}, reverse = True):
        # first handle deletes, they are indexed based on the old indexes
        #for change in sorted(changes, key=lambda x: x['path'], reverse=True):
        for change in sorted(changes, key=functools.cmp_to_key(sortpaths)):
            if change['type']!='deleted': continue
            if len(change['path'])!=l: continue
            obj=getitem(res,change['path'][:-1])
            if obj is None:
                print("could not resolve path '%s', action: %s\ndata: %s" % (change['path'], change['type'], change['data']))
                return
            if isinstance(obj,dict) and change['path'][-1] not in obj:
                print("cannot delete %s what is not there in %s" % (change['path'][-1], change['data']))
                print(change,obj)
                return
            elif isinstance(obj,list) and change['path'][-1]>=len(obj):
                print("cannot delete %s what is not there in %s" % (change['path'][-1], change['data']))
                print(change,obj)
                return
            elif change['data']==obj[change['path'][-1]]:
                #print("\tdeleting", change['path'])
                del obj[change['path'][-1]]
            else:
                print("wtf deleted: %s\nobj: %s" % (change, obj))

    for l in sorted({len(x['path']) for x in changes}):
        # handle adds
        for change in sorted(changes, key=lambda x: x['path']):
            if change['type']!='added': continue
            if len(change['path'])!=l: continue
            obj=getitem(res,change['path'][:-1])
            if obj is None:
                print("could not resolve path '%s', action: %s\ndata: %s" % (change['path'], change['type'], change['data']))
                #print(list(x['path'] for x in sorted(changes, key=functools.cmp_to_key(sortpaths))))
                return
            #print("\tadding", change['path'])
            if isinstance(obj,list):
                obj.insert(change['path'][-1],deepcopy(change['data']))
            else:
                obj[change['path'][-1]]=deepcopy(change['data'])

        # handle changes
        for change in changes:
            if change['type']!='changed': continue
            if len(change['path'])!=l: continue
            obj=getitem(res,change['path'][:-1])
            if obj is None:
                print("could not resolve path '%s', action: %s\ndata: %s" % (change['path'], change['type'], change['data']))
                return
            if isinstance(obj,dict) and change['path'][-1] not in obj:
                print("cannot change %s what is not there in %s" % (change['path'][-1], change['data']))
                return
            elif isinstance(obj,list) and change['path'][-1]>=len(obj):
                print("cannot change %s what is not there in %s" % (change['path'][-1], change['data']))
                return
            elif obj[change['path'][-1]]==change['data'][0]:
                #print("\tchanging", change['path'])
                obj[change['path'][-1]]=deepcopy(change['data'][1])
            else:
                print("wtf change", change, obj)
    return res

# todo write tests for revert
def revert(obj, changes):
    res = deepcopy(obj)
    #clen = len(changes)
    for l in sorted({len(x['path']) for x in changes}, reverse=True):
        # handle changes
        for change in changes:
            if change['type']!='changed': continue
            if len(change['path'])!=l: continue
            obj=getitem(res,change['path'][:-1])
            if obj is None:
                if debug: print("could not resolve path '%s', action: %s\ndata: %s" % (change['path'], change['type'], change['data']))
                raise ValueError()
                return
            if isinstance(obj,dict) and change['path'][-1] not in obj:
                if debug: print("cannot change path: %s what is not there in %s" % (change['path'][-1], change['data']))
                raise ValueError()
                return
            elif isinstance(obj,list) and change['path'][-1]>=len(obj):
                if debug: print("cannot change path: %s what is not there in %s" % (change['path'][-1], change['data']))
                raise ValueError()
                return
            elif obj[change['path'][-1]]==change['data'][1]:
                #print("\tchanging", change['path'])
                obj[change['path'][-1]]=deepcopy(change['data'][0])
            else:
                if debug: print("wtf change: %s\nobj: %s" % (change, obj))
                raise ValueError()

        # undo adds, they are indexed based on the new indexes
        for change in sorted(changes, key=functools.cmp_to_key(sortpaths)):
            if change['type']!='added': continue
            if len(change['path'])!=l: continue
            obj=getitem(res,change['path'][:-1])
            if obj is None:
                print("could not resolve path '%s', action: %s\ndata: %s" % (change['path'], change['type'], change['data']))
                return (i,clen)

            if isinstance(obj,dict) and change['path'][-1] not in obj:
                print("cannot delete %s what is not there in %s" % (change['path'][-1], change['data']))
                return
            elif isinstance(obj,list) and change['path'][-1]>=len(obj):
                print("cannot delete %s what is not there in %s" % (change['path'][-1], change['data']))
                return
            elif change['data']==obj[change['path'][-1]]:
                #print("\tdeleting", change['path'])
                del obj[change['path'][-1]]
            else:
                print("wtf add: %s\nobj: %s" % (change, obj))

        # undo deletes
        for change in sorted(changes, key=lambda x: x['path']):
            if change['type']!='deleted': continue
            if len(change['path'])!=l: continue
            obj=getitem(res,change['path'][:-1])
            if obj is None:
                print("could not resolve path '%s', action: %s\ndata: %s" % (change['path'], change['type'], change['data']))
                #print(list(x['path'] for x in sorted(changes, key=functools.cmp_to_key(sortpaths))))
                return
            #print("\tadding", change['path'])
            if isinstance(obj,list):
                obj.insert(change['path'][-1],deepcopy(change['data']))
            else:
                obj[change['path'][-1]]=deepcopy(change['data'])

    #print(dumps(res))
    return res

# todo stuff starts here
#
#
# todo test printing of diffs
#def printdict(d,i=0, suppress=[]):
#    if type(d)==type(list()):
#        return (u'\n\t%s' % ('  '*i)).join([printdict(v,i+1 ) for v in d])
#    if not type(d) in [dict, hashabledict]:
#        return d
#    res=['']
#    for k,v in [(k,v) for k,v in d.items() if k not in suppress]:
#        res.append(u"\t%s%s:\t%s" % ('  '*i,k,printdict(v,i+1)))
#    return u'\n'.join(res)
#
#def showdiff(item,diffs):
#    if debug: pprint.pprint(diffs)
#    #pprint.pprint(diffs)
#    if debug: print()
#    if debug: pprint.pprint(item)
#    if debug: print()
#    if debug: pprint.pprint(offsetd)
#    res={}
#    for change in diffs:
#        if debug: pprint.pprint( change )
#        # added dicts should be terminal
#        if change['type'] in ['added', 'deleted'] and type(change['data'])==type(dict()):
#            if len(change['path'])>1:
#                tmpk=tuple(change['path'][:-1])
#            else:
#                tmpk=tuple(change['path'])
#            if not tmpk in res:
#                res[tmpk]=(change['data'], [change])
#            else:
#                res[tmpk][1].append(change)
#            continue
#        elem=item
#        deleted=False
#        # find the parent element of the changed one
#        for k in change['path'][:-1]:
#            try:
#                elem=elem[k]
#            except (KeyError, IndexError):
#                # whoops, should not happen, really.
#                deleted=True
#                print("!!!Deleted", k)
#                print(change)
#                print(elem)
#                break
#        if debug: pprint.pprint( elem )
#        if not deleted:
#            if not tuple(change['path'][:-1]) in res:
#                res[tuple(change['path'][:-1])]=(elem, [])
#            res[tuple(change['path'][:-1])][1].append(change)
#            if debug: pprint.pprint(elem[change['path'][-1]])
#        if debug: print()
#    # print result as ascii
#    result=[]
#    for path, (elem, changes) in sorted(res.items()):
#        result.append('/'.join(map(str,path)))
#        skip=False
#        for c in changes:
#            if c['type']=='added':
#                if type(c['data'])==type(dict()):
#                    result.append( "+\t%s" % "\n+\t".join(printdict(c['data']).split('\n')))
#                    skip=True
#                    continue
#                else:
#                    result.append( '+\t%s: <strong>%s</strong>' % (c['path'][-1],"\n+\t".join(printdict(c['data']).split('\n'))))
#            elif c['type']=='deleted':
#                if type(c['data'])==type(dict()):
#                    result.append( "-\t%s" % "\n-\t".join(printdict(c['data']).split('\n')))
#                    skip=True
#                    continue
#                else:
#                    #import code; code.interact(local=locals());
#                    if debug: pprint.pprint(c['data'])
#                    result.append( '-\t%s: <del>%s</del>' % (c['path'][-1],"\n-\t".join(printdict(c['data']).split('\n'))))
#            elif c['type']=='changed':
#                result.append( '!\t%s: <strong>%s</strong><del>%s</del>' % (c['path'][-1],"\n!\t".join(printdict(c['data'][1]).split('\n')),"\n!\t".join(printdict(c['data'][0]).split('\n'))))
#            else:
#                continue # ignore/suppress unknown types
#            if type(elem)==type(dict()) and c['path'][-1] in elem:
#                del elem[c['path'][-1]]
#        if not skip and not type(elem)==type(list()):
#            result.append(printdict(elem))
#    return '\n'.join(result)
#
#def textdiff(d):
#    res=[]
#    for di in sorted(d,key=itemgetter('path')):
#        if 'text' in di['path'] or 'summary' in di['path']:
#            res.append(u'\nsummary text changed in %s' % u'/'.join([str(x) for x in di['path']]))
#            continue
#        if di['type']=='changed':
#            res.append(u'\nchanged %s from:\n\t%s\n  to:\n\t%s' % (u'/'.join([str(x) for x in di['path']]),di['data'][0],printdict(di['data'][1])))
#            continue
#        res.append(u"\n%s %s:\t%s" % (di['type'], u'/'.join([str(x) for x in di['path']]), printdict(di['data'])))
#    return '\n'.join(res)


if __name__ == "__main__":
    import sys, json
    argc=len(sys.argv)
    if argc!=4:
        print("%s diff old new\n%s patch old diff\n%s revert new diff")

    with open(sys.argv[2], 'r') as fd:
        a = json.load(fd)
    with open(sys.argv[3], 'r') as fd:
        b = json.load(fd)

    if sys.argv[1] == 'diff':
        print(json.dumps(diff(a,b)))
    elif sys.argv[1] == 'patch':
        print(json.dumps(patch(a,b)))
    elif sys.argv[1] == 'revert':
        print(json.dumps(revert(a,b)))
