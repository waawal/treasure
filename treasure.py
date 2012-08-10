

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


def get_meta(name, version, service=PYPI_SERVICE):
    client = xmlrpclib.ServerProxy(service)
    try:
        meta = client.release_data(name, version)
    except TypeError: # Sometimes None is returned from PYPI as the version.
        version = client.package_releases(name)[0]
        meta = client.release_data(name, version)
    return meta

def process_update_queue(queue, classifiers=CLASSIFIER, ):
    result = []
    for updated in queue: # Updates can come before new.
        name, version = updated
        meta = get_meta(name, version, client)
        if classifiers.intersection(meta.get('classifiers')):
            result.append(name, meta)
    return result

def check_for_updates(supported, classifiers=CLASSIFIERS,
                      interval=QUERY_INTERVAL, service=PYPI_SERVICE):
    """ Checks for new projects and updates.
        Returns the overall processingtime in seconds.
    """
    firstrun = True
    while True:
        if not firstrun:
            endprocessing = time()
            processingtime = endprocessing - startprocessing
        sleep(processingtime)
        result = []
        startprocessing = time() # Let's do this!
        client = xmlrpclib.ServerProxy(service)
        since = int(startprocessing - interval)
        updates = client.changelog(since)
        # [['vimeo', '0.1.2', 1344087619,
        # 'update description, classifiers'], ...]]
        
        if updates:
            queue = deque() # Since actions can share timestamp.

            for module in updates:
                name, version, timestamp, actions = module
                if name not in supported:
                    if 'create' in actions:
                        queue.appendleft((name, version))
                    elif 'new release' in actions or 'classifiers' in actions:
                        queue.append((name, version))
                result = process_update_queue(queue)
            try:
                if result:
                    yield queue.next()
            except StopIteration:
                continue
        
        if firstrun:
            firstrun = False


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
        for module in check_for_updates(supported)
            print module

