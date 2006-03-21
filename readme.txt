Zope Debugger

  Enhancements for debugging Zope using Python's debugger.

  To install, unpack the zdb tarball into the Products directory of
  your instance and restart Zope. Once restarted, you should visit
  /manage_addProduct/zdb/debug_compile of your server in a
  browser.

  To use, in any code which you would like to debug, just insert the
  following lines:

  from Products.zdb import set_trace
  set_trace()

  NB: Having zdb installed will decrease performance slightly and
      increase RAM usage proportional to the number of scripts you
      use. It should ONLY be installed on servers where you need to
      carry out debugging!

  Known Problems

     zdb is currently incompatible with the WingDbg product that ships
     with WingIDE. Contact has been made with WingIDE's authors to try
     and resolve this problem. 

  Licensing

     Copyright (c) 2005 Simplistix Ltd

     This Software is released under the MIT License:
     http://www.opensource.org/licenses/mit-license.html
     See license.txt for more details.

  Changes
 
     0.8.2

       - Added compatability with Zope 2.9 and Python 2.4

     0.8.1

       - Added compatibility with both Zope 2.7 and Zope 2.8

       - Noted incompatability with WingIDE's WingDbg product.

       - Fixed documentation of how to run the debug_compile script. 

     0.8.0 

       - Initial Release featuring the ability to set break points and
         view source code locations within Script (Python)'s and
         FSPythonSCript's

  Credits

    - Dieter Maurer for the inspiration that this was possible. 

    - Tres Seaver and Jim Fulton for their help ironing out the
      wrinkles.

    - The excellent Plone Conference in Vienna, 2005, for a great place
      to write the code!

  To-Do

    - Add traceback improvements such as ZPT hints into pdb's stack traces

    - Add traceback improvements such as ZPT hints into the traceback
      module's exception formatting
