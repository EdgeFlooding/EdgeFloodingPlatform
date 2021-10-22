
from frame import Frame
from threading import Lock
import time

def synchronized(lock):
    """ Synchronization decorator. """

    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap


'''
Each slot contains only the most recent frame produced.
It also keeps track of the number of frames produced.
'''
class FrameSlot():

    # does it store a new frame?
    empty = True
    lock = Lock()
    # counters to track frames produced and consumed
    frames_produced = 0
    frames_consumed = 0


    def __init__(self, id):
        # id to identify which camera is producing to this slot
        self.id = id
        self.frame_object = Frame(id)
        

    # called by the producer
    @synchronized(lock)
    def update_frame(self, raw_frame):
        self.empty = False
        self.frame_object.raw_frame = raw_frame
        self.frame_object.creation_timestamp = time.time()
        self.frames_produced = self.frames_produced + 1
        #print("Frame prodotti: ", self.frames_produced)


    # called by the consumer
    @synchronized(lock)
    def consume_frame(self):
        if self.empty == True:
            # skip this slot
            return None
        
        self.empty = True
        self.frame_object.service_timestamp = time.time()
        self.frames_consumed = self.frames_consumed + 1
        #print("Frame consumati: ", self.frames_consumed)

        return self.frame_object

