import time
from threading import Thread, Event, Semaphore

def count_down(n, event):
	print('count_down starting')
	event.set()
	while n > 0:
		print('T-minus', n)
		n -= 1
		time.sleep(3)


class CountDownTask:
	def __init__(self):
		self.running = True
	def terminate(self):
		self.running = False
	def run(self, n):
		while self.running and n > 0:
			print('T-minus', n)
			n -= 1
			time.sleep(1)


def worker(n, sema):
	sema.acquire()
	print('Working', n)

sema = Semaphore(0)
nworkers = 10


if __name__ == '__main__':
	#print('Launching count_down')
	#event = Event()
	#t = Thread(target=count_down, args=(5, event))
	#t.start()
	#event.wait()
	#print('count_down is running')
	for n in range(nworkers):
		t = Thread(target=worker, args = (n, sema,))
		t.start()
