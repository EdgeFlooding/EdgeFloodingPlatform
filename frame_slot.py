from frame import Frame
from threading import Lock
import time
from collections import deque

def current_time_int():
    return int(round(time.time() * 1000_000_000))


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

    lock = Lock()
    frame_buffer = None
    # counters to track frames produced and consumed
    frames_produced = 0
    frames_consumed = 0


    def __init__(self, id, length_buffer):
        # id to identify which camera is producing to this slot
        self.id = id
        self.frame_buffer = deque(maxlen=length_buffer)


    # called by the producer
    @synchronized(lock)
    def update_frame(self, frame : Frame):
        
        # Check for id mismatch
        if frame.id_slot != self.id:
            print(f"[ERROR] The Frame with id_slot: {frame.id_slot} cannot be insertid in FrameSlot: {self.id}")
            return

        # Updating the frame_buffer
        self.frame_buffer.appendleft(frame)

        self.frames_produced = self.frames_produced + 1
        #print("Frame prodotti: ", self.frames_produced)


    # called by the consumer
    @synchronized(lock)
    def consume_frame(self):
        if len(self.frame_buffer) == 0:
            # skip this slot
            return None

        self.frames_consumed = self.frames_consumed + 1
        #print("Frame consumati: ", self.frames_consumed)

        # pop the frame from the head of the fifo queue
        return_obj = self.frame_buffer.pop()
        # Remember to set the service timestamp
        return_obj.service_timestamp = current_time_int()

        return return_obj

