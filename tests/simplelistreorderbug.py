#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# throws

import datetime, json
from objchanges import diff, patch

def test(a, b):
    print("x"*80)
    print("a", a)
    print("")
    print("b", b)
    print("")
    print("_"*120)
    d = diff(a,b)
    #print("")
    for x in sorted(d,key=lambda x: len(x['path'])): print(x)
    #print("")
    p = patch(a, d)
    assert p is not None
    tmp = diff(p,b)
    if len(tmp) != 0:
        print("_"*120)
        print("patch(a, diff(a,b))!=b")
        print("b2", p)
        print("diff")
        for x in sorted(tmp,key=lambda x: len(x['path'])): print(x)
    assert (tmp==[])

new={
 "committees": [
  {
   "com": "JURI",
   "rap": [{ "name": "BARLEY" }],
  },
  {
   "com": "LIBE",
   "rap": [
    { "name": "BARLEY" }
   ],
  }
 ]
}
old={
 "committees": [
  {
   "com": "LIBE",
   "rap": [{ "name": "BARLEY", }],
  },
  {
   "com": "JURI",
   "rap": [
    { "name": "BARLEY", },
    { "name": "HAUTALA", }
   ],
  },
 ]
}
test(old,new)


