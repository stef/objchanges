!objchanges

can diff simple python objects consisting only of dicts/lists/atomic types, but
is also able to apply the diffs as patches to existing objects. also included
is a fuzzer that creates random objects to test objchanges.

if the objects are supported this should work fine
```
    assert diff(new, patch(old, diff(old, new))) in [None, []]
```
