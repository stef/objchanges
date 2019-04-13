#!/usr/bin/env python3
# throws

from objchanges import diff, patch

def test(a, b):
    #print("x"*80)
    #print("a", a)
    #print("")
    #print("b", b)
    #print("")
    #print("_"*120)
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

old = {"procedure": {"subject": ["3.50.01.05 Research specific areas", "3.50.08 New technologies, biotechnology", "3.50.20 Scientific and technological cooperation and agreements", "3.60.04 Nuclear energy, industry and safety", "8.70 Budget of the Union", "8.70.02 Financial regulations"]}}
new = {"procedure": {"subject": ["3.50.20 Scientific and technological cooperation and agreements", "3.60.15 Cooperation and agreements for energy", "8.70 Budget of the Union"]}}
test(old,new)

#old = "subject":                                                               new = "subject":
#     ["3.50.01.05 Research specific areas",                                  -
#     "3.50.08 New technologies, biotechnology",                              -
#     "3.50.20 Scientific and technological cooperation and agreements",      =     ["3.50.20 Scientific and technological cooperation and agreements",
#     "3.60.04 Nuclear energy, industry and safety",                          +      "3.60.15 Cooperation and agreements for energy",
#     "8.70 Budget of the Union",                                             =      "8.70 Budget of the Union"]
#     "8.70.02 Financial regulations"]                                        -
#
# diff
# {'type': 'deleted', 'path': ['procedure', 'subject', 0], 'data': '3.50.01.05 Research specific areas'}
# {'type': 'added', 'path': ['procedure', 'subject', 1], 'data': '3.50.01.05 Research specific areas'}
# {'type': 'changed', 'path': ['procedure', 'subject', 1], 'data': ('3.50.08 New technologies, biotechnology', '3.60.15 Cooperation and agreements for energy')}
# {'type': 'deleted', 'path': ['procedure', 'subject', 1], 'data': '3.50.08 New technologies, biotechnology'}
# {'type': 'deleted', 'path': ['procedure', 'subject', 3], 'data': '3.60.04 Nuclear energy, industry and safety'}
# {'type': 'deleted', 'path': ['procedure', 'subject', 5], 'data': '8.70.02 Financial regulations'}

old = {"procedure": {"subject": ["3.50.01.05 Research specific areas", "3.50.08 New technologies, biotechnology", "3.60.04 Nuclear energy, industry and safety", "8.70 Budget of the Union", "8.70.02 Financial regulations", "3.50.20 Scientific and technological cooperation and agreements"]}}
new = {"procedure": {"subject": ["3.50.20 Scientific and technological cooperation and agreements", "3.60.15 Cooperation and agreements for energy", "8.70 Budget of the Union"]}}
test(old,new)

def dump(a,b):
    for i,j in zip(a['procedure']['subject'],b['procedure']['subject']):
        print("%80s %80s" % (i,j))

dump(new,patch(old, diff(old,new)))
