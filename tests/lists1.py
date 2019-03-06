#!/usr/bin/env python3
# throws

from objchanges import diff, patch

def test(a, b):
    print("x"*80)
    #for i, x in enumerate(a): print("%2d" % i,sorted(x.items()))
    #print("")
    #for i, x in enumerate(b): print("%2d" % i,sorted(x.items()))
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
        print("b2")
        for i, x in enumerate(p): print("%2d" % i,sorted(x.items()))
        print("b")
        for i, x in enumerate(b): print("%2d" % i,sorted(x.items()))
        print("diff")
        for x in sorted(tmp,key=lambda x: len(x['path'])): print(x)
    assert (tmp==[])

old=[{'end': '1989-07-24', 'committee_id': 'BUDG', 'start': '1987-01-21', 'role': 'Member', 'abbr': 'BUDG', 'Organization': 'Budgets'}, {'Organization': 'Institutional Affairs', 'role': 'Substitute', 'end': '1989-07-24', 'abbr': None, 'start': '1987-01-21'}, {'end': '1987-01-20', 'committee_id': 'BUDG', 'start': '1984-07-26', 'role': 'Member', 'abbr': 'BUDG', 'Organization': 'Budgets'}]
new=[{'role': 'Member', 'Organization': 'Budgets', 'start': '1984-07-26', 'end': '1987-01-20', 'term': 2, 'abbr': 'BUDG'}, {'role': 'Member', 'Organization': 'Budgets', 'start': '1987-01-21', 'end': '1989-07-24', 'term': 2, 'abbr': 'BUDG'}, {'role': 'Substitute', 'Organization': 'Development and Cooperation', 'start': '1984-09-24', 'end': '1987-01-20', 'term': 2, 'abbr': ''}]
test(old,new)
