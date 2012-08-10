

import xmlrpclib
from collections import deque
from time import time, sleep

QUERY_INTERVAL = 2 * 60 # In seconds, intervals between queries to PYPI, 2 min.
PYPI_SERVICE = 'http://pypi.python.org/pypi'
CLASSIFIERS = frozenset(('Programming Language :: Python :: 3',
                         'Programming Language :: Python :: 3.0',
                         'Programming Language :: Python :: 3.1',
                         'Programming Language :: Python :: 3.2',
                         'Programming Language :: Python :: 3.3',
                         ))


def get_meta(name, version, client):
    try:
        meta = client.release_data(name, version)
    except TypeError: # Sometimes None is returned from PYPI as the version.
        version = client.package_releases(name)[0]
        meta = client.release_data(name, version)
    return meta

def check_for_updates(supported, classifiers=CLASSIFIERS,
                      interval=QUERY_INTERVAL, service=PYPI_SERVICE):
    """ Checks for new projects and updates.
        Returns the overall processingtime in seconds.
    """
    startprocessing = time() # Let's do this!
    client = xmlrpclib.ServerProxy(service)
    since = int(startprocessing - interval)
    updates = client.changelog(since)
    # [['vimeo', '0.1.2', 1344087619,'update description, classifiers'], ...]]
    
    if updates:
        print updates # Log to heroku.
        queue = deque() # Since actions can share timestamp.

        for module in updates:
            name, version, timestamp, actions = module
            if name not in supported:
                if 'create' in actions:
                    queue.appendleft((name, version))
                elif 'new release' in actions or 'classifiers' in actions:
                    queue.append((name, version))

        for updated in queue: # Updates can come before new.
            name, version = updated
            meta = get_meta(name, version, client)
            if classifiers.intersection(meta.get('classifiers')):
                supported.add(name)
                post_to_twitter(name, meta)

    endprocessing = time()
    processingtime = endprocessing - startprocessing
    return processingtime

def get_supported(classifiers=CLASSIFIERS, service=PYPI_SERVICE):
    """ Builds a set of the PYPI-projects currently listed under the provided
        classifiers.
    """
    client = xmlrpclib.ServerProxy(service)
    multicall = xmlrpclib.MultiCall(client)
    [multicall.browse([classifier]) for classifier in classifiers]
    supported = set()
    for results in multicall(): # Returns a list of ['projectname', 'version']
        supported = supported.union([result[0] for result in results])
    return supported


if __name__ == '__main__':
    supported = get_supported()
    sleep(QUERY_INTERVAL)
    while True:
        processingtime = check_for_updates(supported)
        sleep(QUERY_INTERVAL - processingtime) # Consider processing time.

