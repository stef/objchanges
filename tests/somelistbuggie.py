#!/usr/bin/env python3
# throws

import datetime
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

old=[{'type': 'Responsible Committee', 'body': 'EP', 'committee_full': 'International Trade', 'committee': 'INTA', 'associated': False, 'date': ['2018-02-19T00:00:00'], 'rapporteur': [{'name': 'LANGE Bernd', 'mepref': 1909, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}]}]
new=[{'type': 'Responsible Committee', 'body': 'EP', 'committee_full': 'Development', 'committee': 'DEVE', 'associated': False, 'date': ['2018-03-20T00:00:00'], 'rapporteur': [{'name': 'MCAVAN Linda', 'mepref': 2327, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}], 'shadows': [{'name': 'ZAHRADIL Jan', 'mepref': 23712, 'group': 'European Conservatives and Reformists', 'abbr': 'ECR'}]}, {'type': 'Committee Opinion', 'body': 'EP', 'committee_full': 'International Trade', 'committee': 'INTA', 'associated': False, 'date': ['2018-02-19T00:00:00'], 'rapporteur': [{'name': 'LANGE Bernd', 'mepref': 1909, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}]}]
test(old,new)


# old
#[{'type': 'Responsible Committee',
#  'body': 'EP',
#  'committee_full': 'International Trade',
#  'committee': 'INTA',
#  'associated': False,
#  'date': ['2018-02-19T00:00:00'],
#  'rapporteur': [{'name': 'LANGE Bernd',
#                  'mepref': 1909,
#                  'group': 'Progressive Alliance of Socialists and Democrats',
#                  'abbr': 'S&D'}]}]

# diff
#{'type': 'deleted', 'path': [0], 'data': {'type': 'Responsible Committee', 'body': 'EP', 'committee_full': 'International Trade', 'committee': 'INTA', 'associated': False, 'date': ['2018-02-19T00:00:00'], 'rapporteur': [{'name': 'LANGE Bernd', 'mepref': 1909, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}]}}
#{'type': 'added', 'path': [1], 'data': {'type': 'Responsible Committee', 'body': 'EP', 'committee_full': 'International Trade', 'committee': 'INTA', 'associated': False, 'date': ['2018-02-19T00:00:00'], 'rapporteur': [{'name': 'LANGE Bernd', 'mepref': 1909, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}]}}
#{'type': 'added', 'path': [0], 'data': {'type': 'Responsible Committee', 'body': 'EP', 'committee_full': 'Development', 'committee': 'DEVE', 'associated': False, 'date': [datetime.datetime(2018, 3, 20, 0, 0)], 'rapporteur': [{'name': 'MCAVAN Linda', 'mepref': 2327, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}], 'shadows': [{'name': 'ZAHRADIL Jan', 'mepref': 23712, 'group': 'European Conservatives and Reformists', 'abbr': 'ECR'}]}}
#{'type': 'changed', 'path': [1, 'type'], 'data': (None, 'Committee Opinion')}

# new
#[{'type': 'Responsible Committee',
#  'body': 'EP',
#  'committee_full': 'Development',
#  'committee': 'DEVE',
#  'associated': False,
#  'date': [datetime.datetime(2018, 3, 20, 0, 0)],
#  'rapporteur': [{'name': 'MCAVAN Linda', 'mepref': 2327, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}],
#  'shadows': [{'name': 'ZAHRADIL Jan', 'mepref': 23712, 'group': 'European Conservatives and Reformists', 'abbr': 'ECR'}]},
# {'type': 'Committee Opinion',
#  'body': 'EP',
#  'committee_full': 'International Trade',
#  'committee': 'INTA',
#  'associated': False,
#  'date': [datetime.datetime(2018, 2, 19, 0, 0)],
#  'rapporteur': [{'name': 'LANGE Bernd', 'mepref': 1909, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}]}]

# patched old
# [{'type': 'Responsible Committee',
#   'body': 'EP',
#   'committee_full': 'Development',
#   'committee': 'DEVE',
#   'associated': False,
#   'date': [datetime.datetime(2018, 3, 20, 0, 0)],
#   'rapporteur': [{'name': 'MCAVAN Linda', 'mepref': 2327, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}],
#   'shadows': [{'name': 'ZAHRADIL Jan', 'mepref': 23712, 'group': 'European Conservatives and Reformists', 'abbr': 'ECR'}]},
#  {'type': 'Responsible Committee',
#   'body': 'EP',
#   'committee_full': 'International Trade',
#   'committee': 'INTA',
#   'associated': False,
#   'date': ['2018-02-19T00:00:00'],
#   'rapporteur': [{'name': 'LANGE Bernd', 'mepref': 1909, 'group': 'Progressive Alliance of Socialists and Democrats', 'abbr': 'S&D'}]}]
