from Acquisition import aq_parent
from Products.PythonScripts.PythonScript import PythonScript

import linecache
import os
import sys
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
    size = len(self._body)
    # don't do anything if we get no body
    if not size:
        return
    mtime = 0
    filename = '/'.join(self.getPhysicalPath())
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

# CMF-specific bits
try:
    from Products.CMFCore.FSPythonScript import FSPythonScript
except ImportError:
    # a dummy class, so isinstance lower down should never return true
    class FSPythonScript:
        pass
else:
    original_write = FSPythonScript._write
     # this is where we fill the line cache for FS Python Scripts
    def monkey_write(self,text,compile):
        original_write(self,text,compile)
        self._fillLineCache()

    FSPythonScript._write = monkey_write
    FSPythonScript._fillLineCache = monkey_fillLineCache

def monkey_compiler(self, *args, **kw):
    if self._body:
        # only do something if we have a body to play with
        if aq_parent(self) is None:
            # we have a body but no acquisiton context,
            # we're either something to do with an
            # FSPythonScript, or being called from within
            # __setstate__ due to a change in Python_magic or Script_magic

            # try and find an FSPythonScript in our call stack
            try:
                raise ZeroDivisionError
            except ZeroDivisionError:
                f = sys.exc_info()[2].tb_frame
                while f:
                    obj = f.f_locals.get('self')
                    if isinstance(obj,FSPythonScript):
                        break
                    f = f.f_back
                if f is None:
                    filename = 'Python Script without Acquisition Context'
                else:
                    filename = '/'.join(obj.getPhysicalPath())
        else:
            filename = '/'.join(self.getPhysicalPath())

        args = list(args)
        args[3]=filename

    return RestrictedPython.compile_restricted_function(*args, **kw)

PythonScript._compiler = monkey_compiler


