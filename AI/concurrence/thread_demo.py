
import time
from threading import Thread, Semaphore


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


if __name__ == '__main__':
    semaphore = Semaphore(0)
    worker_num = 10
    for i in range(worker_num):
        t = Thread(target=worker, args=(i, semaphore,))
        t.start()
