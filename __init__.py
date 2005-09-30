# Copyright (c) 2005 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
from AccessControl import ModuleSecurityInfo
from App.FactoryDispatcher import FactoryDispatcher
from bdb import Bdb
from cmd import Cmd
from pdb import Pdb

import monkeypatch
import sys

class Zdb(Pdb):

    def __init__(self):
        Bdb.__init__(self)
        Cmd.__init__(self)
        self.rcLines = []
        self.prompt = '(zdb) '
        self.aliases = {}

    def canonic(self, filename):
        if monkeypatch.ps_fncache.has_key(filename):
            return filename
        return Pdb.canonic(self,filename)

    # Python 2.4's bdb set_trace method
    # This can go away when Python 2.3 is no longer supported
    def set_trace(self, frame=None):
        """Start debugging from `frame`.

        If frame is not specified, debugging starts from caller's frame.
        """
        if frame is None:
            frame = sys._getframe().f_back
        self.reset()
        while frame:
            frame.f_trace = self.trace_dispatch
            self.botframe = frame
            frame = frame.f_back
        self.set_step()
        sys.settrace(self.trace_dispatch)

# make us "safe"
ModuleSecurityInfo('Products.zdb').declarePublic('set_trace')
def set_trace():
    Zdb().set_trace(sys._getframe().f_back)

# recompilation utlitity
def initialize(context):
    # This horrificness is required because Zope doesn't understand the concept
    # of a Product that doesn't register any classes :-(
    pack=context._ProductContext__pack
    fd=getattr(pack, '__FactoryDispatcher__', None)
    if fd is None:
        class __FactoryDispatcher__(FactoryDispatcher):
            "Factory Dispatcher for a Specific Product"

        fd = pack.__FactoryDispatcher__ = __FactoryDispatcher__

    if not hasattr(pack, '_m'): pack._m=fd.__dict__
    setattr(fd,'debug_compile',debug_compile)
    setattr(fd,'debug_compile__roles__',('Manager',))

# utility stuff

def debug_compile(self):
    '''Recompile all Python Scripts'''
    base = self.this()
    scripts = base.ZopeFind(base, obj_metatypes=('Script (Python)',),
                            search_sub=1)
    names = []
    for name, ob in scripts:
        names.append(name)
        ob._compile()
        ob._p_changed = 1

    if names:
        return 'The following Scripts were recompiled:\n' + '\n'.join(names)
    return 'No Scripts were found.'
