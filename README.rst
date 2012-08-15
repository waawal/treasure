=====================================
Treasure - The PYPI-bot
=====================================
:Info: Read the `documentation <http://treasure.readthedocs.org>`_ hosted at readthedocs.
:Author: Daniel Waardal


Trove
  *n.*  
  A collection of valuable items discovered or found; a treasure-trove.


Examples
--------

::

    from pprint import pprint
    from treasure import troves
    
    CLASSIFIERS = ('Topic :: Internet :: WWW/HTTP :: WSGI',
              Topic :: Internet :: WWW/HTTP :: WSGI :: Application,
              Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware,
              Topic :: Internet :: WWW/HTTP :: WSGI :: Server,
              )
    
    for result in troves(CLASSIFIERS):
        pprint result

Reference:
  http://pypi.python.org/pypi?%3Aaction=list_classifiers
