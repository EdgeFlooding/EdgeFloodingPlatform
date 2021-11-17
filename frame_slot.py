
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
    frame_object = Frame()
    # counters to track frames produced and consumed
    frames_produced = 0
    frames_consumed = 0


    def __init__(self, id):
        # id to identify which camera is producing to this slot
        self.id = id


    # called by the producer
    @synchronized(lock)
    def update_frame(self, frame : Frame):
        
        if frame.id_slot != self.id:
            print(f"[ERROR] The Frame with id_slot: {frame.id_slot} cannot be insertid in FrameSlot: {self.id}")
            return
        
        self.empty = False

        # Updating the frame_object
        self.frame_object = frame

        self.frames_produced = self.frames_produced + 1
        #print("Frame prodotti: ", self.frames_produced)


    # called by the consumer
    @synchronized(lock)
    def consume_frame(self):
        if self.empty == True:
            # skip this slot
            return None

        self.empty = True

        self.frames_consumed = self.frames_consumed + 1
        #print("Frame consumati: ", self.frames_consumed)

        # I need to return a new Frame obj to avoid working on the same reference
        return_obj = Frame()
        return_obj.copy_attributes(self.frame_object)
        # Remember to set the service time stamp
        return_obj.service_timestamp = time.time()

        return return_obj

