import gevent
import random
import time

def task(pid):
	gevent.sleep(random.randint(0,2) * 0.001);
	print('Tast %s done' % pid);

def synchronous():
	for i in range(1,10):
		task(i)

def asynchronous():
	gevent.joinall([gevent.spawn(task,i) for i in xrange(10)])


asynchronous();


print end1, end2;
