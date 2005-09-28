from Products.PythonScripts.PythonScript import PythonScript

import linecache
import os
import RestrictedPython

ps_fncache = {}

def monkey_checkcache():
    """Discard cache entries that are out of date...
    ...and aren't PythonScripts!"""

    for filename in linecache.cache.keys():
        size, mtime, lines, fullname = linecache.cache[filename]
        if mtime==0:
            continue
        try:
            stat = os.stat(fullname)
        except os.error:
            del linecache.cache[filename]
            continue
        if size != stat.st_size or mtime != stat.st_mtime:
            del linecache.cache[filename]

linecache.checkcache = monkey_checkcache


def monkey_fillLineCache(self):
    filename = '/'.join(self.getPhysicalPath())
    size = len(self._body)
    mtime = 0
    lines = [l+'\n' for l in self._body.split('\n')]
    fullname = 'Script (Python) at '+filename
    linecache.cache[filename] = size, mtime, lines, fullname
    ps_fncache[filename]=True
PythonScript._fillLineCache = monkey_fillLineCache

    
original_exec = PythonScript._exec

def monkey_exec(self, bound_names, args, kw):
    self._fillLineCache()
    return original_exec(self, bound_names, args, kw)

PythonScript._exec = monkey_exec

def monkey_compiler(self, *args, **kw):
    self._fillLineCache()
    args = list(args)
    args[3]='/'.join(self.getPhysicalPath())
    return RestrictedPython.compile_restricted_function(*args, **kw)

PythonScript._compiler = monkey_compiler


