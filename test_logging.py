import logging
from time import sleep


logging.basicConfig(level=logging.DEBUG) 

def test_1():
    log = logging.getLogger('test_1')
    log.info('\n\n')
    sleep(1)
    log.debug('after 1 sec')
    sleep(1)
    log.debug('after 2 sec')
    sleep(1)
    log.debug('after 3 sec')
    assert 1, 'should pass'


def test_2():
    log = logging.getLogger('test_2')
    log.info('\n\n')
    sleep(1)
    log.debug('after 1 sec') 
    sleep(1)
    log.debug('after 2 sec')
    sleep(1)
    log.debug('after 3 sec')
    assert 0, 'failing for demo purposes'
