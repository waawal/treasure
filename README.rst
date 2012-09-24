=====================================
Treasure - The PYPI-bot
=====================================
:Info: Read the `documentation <http://treasure.readthedocs.org>`_ hosted at readthedocs.
:Author: Daniel Waardal


Trove
  *n.*  
  A collection of valuable items discovered or found; a treasure-trove.

What is this alla about?
------------------------

This is a module that queries pypi for updates of a sequence of troves during a certain time and processes the difference.

- It isn't using the ``pubsubhubbub`` interface though? - No, not yet at least.

- Why was this created?

* When creating the twitter-bot twittering under the py3k-handle (@py3k) I realized that checking for updates to trove-classifiers on pypi might be interesting for all kinds of bots (IRC, XMPP etc.). That's why this module exist.*

Examples
--------

The documentation will be expanded in the future. Right now I leave you with this:

::

    from pprint import pprint
    from treasure import troves
    
    CLASSIFIERS = ('Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   )
    
    for result in troves(CLASSIFIERS):
        pprint result

Reference:
  http://pypi.python.org/pypi?%3Aaction=list_classifiers
