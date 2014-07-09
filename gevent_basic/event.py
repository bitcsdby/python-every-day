import gevent
from gevent.event import Event
from gevent.event impornt AsyncResult

evt = Event()

def setter1():
	print("A Wait for me");
	gevent.sleep(3)

	print("Setter OK")
	evt.set()

def waiter1():
	print("I am waitting");
	evt.wait();
	print("waiter over");

a = AsyncResult()
def setter2():
	gevent.sleep(3)
	a.set("from setter2")

def waiter2():
	print (a.get())


gevent.joinall([
	gevent.spawn(setter1),
	gevent.spawn(waiter1),
	gevent.spawn(waiter1),
	gevent.spawn(waiter1),
	gevent.spawn(waiter1)
	])

gevent.joinall(
	[
	gevent.spawn(setter2),
	gevent.spawn(waiter2)
	])