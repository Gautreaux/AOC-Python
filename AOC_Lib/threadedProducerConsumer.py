import threading


class ThreadedProducerConsumer:
    # "A thread safe producer comsumer"
    def __init__(self):
        self.lock = threading.Lock()
        self.producerSemaphore = threading.Semaphore(0)
        self.q = []
        self.waitingToRemove = 0
        self.lastInsert = None
        # self.insertHistory = []

    def __len__(self):
        return len(self.q)

    def insert(self, value):
        self.lock.acquire()
        try:
            self.q.append(value)
            self.producerSemaphore.release()
            self.lastInsert = value
            # self.insertHistory.append(value)
        finally:
            self.lock.release()

    def remove(self):
        self.lock.acquire()
        if len(self.q) == 0:
            self.waitingToRemove += 1
            self.lock.release()
            self.producerSemaphore.acquire()
            self.lock.acquire()
            self.waitingToRemove -= 1
        else:
            # just record keeping, we know it will pass
            self.producerSemaphore.acquire()
        try:
            t = self.q[0]
            self.q = self.q[1:]
        finally:
            self.lock.release()
        return t


# TODO - magic functions
#   str
#   repr
