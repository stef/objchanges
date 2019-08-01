!objchanges

can diff simple python objects consisting only of dicts/lists/atomic types, but
is also able to apply the diffs as patches to existing objects. also included
is a fuzzer that creates random objects to test objchanges.

if the objects are supported this should work fine
```
    assert diff(new, patch(old, diff(old, new))) in [None, []]
    assert diff(old, revert(new, diff(old, new))) in [None, []]
```

you can now also display the changes nicely formatted in a ANSI terminal:

```
   old = {...}
   new = {... something changed ... }
   d = diff(old,new)
   print(contextdiff(new, p))
```

!!cmdline

you can also invoke objchanges directly on json files:

```
% cat new
{"a": [{"5": {"1": 3}, "2": {"2": "sZ5"}}, ["ezw", []]], "1": 23, "c": "m0L"}
% cat old
{"a": [{"5": {"1": 3}, "2": {"2": "sZ5"}}, ["ezw"]], "1": 23, "c": "m0L"}

# running simple diff
% ./objchanges.py diff old new
[{"type": "added", "path": ["a", 1], "data": ["ezw", []]}, {"type": "deleted", "path": ["a", 1], "data": ["ezw"]}]

# patching old with diff
% ./objchanges.py patch old <(./objchanges.py diff old new)
{"a": [{"5": {"1": 3}, "2": {"2": "sZ5"}}, ["ezw", []]], "1": 23, "c": "m0L"}

# reverting new with diff
% ./objchanges.py revert new <(./objchanges.py diff old new)
{"a": [{"5": {"1": 3}, "2": {"2": "sZ5"}}, ["ezw"]], "1": 23, "c": "m0L"}

```
