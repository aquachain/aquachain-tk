from queue import Queue
from threading import Thread, Event
from datetime import datetime
from time import sleep
def now():
    return datetime.utcnow()
class LogFilterLooper(Thread):
    def __init__(self, owner, queue, event_filter, duration, aqua=None):
        Thread.__init__(self)
        self.aqua = aqua
        self.queue = queue
        self.owner = owner
        self.duration = duration
        self.event_filter = event_filter
        self._stop_event = Event()
    def run(self):
        print('starting log filter looper thread')
        while self.owner and not self.stopped():
            event = self.event_filter.get_new_entries()
            if len(event) > 0:
                block = self.aqua.gethead()
                self.queue.put(block)
                print(now(),'received new block:', block)
                print('\n')
                self.owner.head = block
                self.owner.rehead()
            sleep(self.duration)

    def stop(self):
        print('stopping log filter looper thread')
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()

class LogQueue(Queue):
    pass
