#!/usr/bin/env python3

# returns a rendering of a set of `changes` for a given object with some ansi color highlighting in the terminal
def contextdiff(obj, changes, tpls=ansi):
    ctree = paths2tree(changes)
    #from pprint import pprint
    #pprint(ctree)
    return walk(obj, ctree, tpls)

# helper for contextdiff
def paths2tree(changes):
    res = {}
    for change in changes:
        path = change['path']
        node = res
        for seg in path:
            if not 'kids' in node:
                node['kids']={}
            if not seg in node['kids']:
                node['kids'][seg]={}
            node = node['kids'][seg]
        if not 'change' in node:
            node['change']=[]
        node['change'].append({'type':change['type'],
                               'data':change['data']})

    return res

ansi = {
    'added': "\033[32m%s\033[0m",    # bg \033[42m
    'deleted': "\033[31m%s\033[0m",  # bg \033[41m
    'changed': "\033[31m%s\033[32m%s\033[0m",
    'indent': "   "
}

# helper for walk
def format_obj(obj, depth, tpls): # todo
    if isinstance(obj, dict):
        return ('\n'+tpls['indent']*(depth))+('\n'+tpls['indent']*(depth)).join(["%s: %s" % (k, format_obj(v, depth+1,tpls)) for k,v in obj.items()])
    if isinstance(obj,list):
        return ('\n'+tpls['indent']*(depth))+('\n'+tpls['indent']*(depth)).join(["%s: %s" % (idx, format_obj(v, depth+1,tpls)) for idx,v in enumerate(obj)])
    return str(obj)

# helper for contextdiff
def walk(node, changes, tpls, depth=0):
    ret = []
    if changes.get('change'):
        for change in  changes['change']:
            if (change['type']) == 'changed':
                ret.append(tpls['changed'] % (format_obj(change['data'][0], depth, tpls), format_obj(change['data'][1], depth, tpls)))
            else:
                ret.append(tpls[change['type']] % format_obj(change['data'], depth, tpls))
    elif changes.get('kids'):
        if isinstance(node, dict):
            for k,v in node.items():
                if k in changes['kids']:
                    ret.append("%s: %s" % (repr(k), walk(node[k], changes['kids'][k], tpls, depth+1)))
                    del changes['kids'][k]
                elif depth>0:
                    if type(v) in (dict, list):
                        ret.append("%s: <unchanged>" % repr(k))
                    else:
                        ret.append("%s: %s" % (repr(k), v))
            for k, change in changes['kids'].items():
                if k in node: continue
                ret.append("%s: %s" % (repr(k), walk({}, change, tpls, depth+1)))
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                if idx in changes['kids']:
                    ret.append("%s: %s" % (repr(idx), walk(node[idx], changes['kids'][idx], tpls, depth+1)))
                else:
                    if type(item) in (dict,list):
                        ret.append("%s:%s<unchanged>" % (repr(idx),('\n'+tpls['indent']*(depth+1))))
                    else:
                        ret.append("%s:%s%s" % (repr(idx), ('\n'+tpls['indent']*(depth+1)), item))
            for k, change in changes['kids'].items():
                if len(node)>k: continue
                ret.append("%s: %s" % (repr(k), walk({}, change, tpls, depth+1)))
        else:
            ret.append("%s" % (node))
    else:
        ret.append("%s: <unchanged>" % (repr(node)))

    return ('\n'+tpls['indent']*(depth))+('\n'+tpls['indent']*(depth)).join(ret)

