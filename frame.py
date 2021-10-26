
from PIL.Image import NONE


class Frame():

    # id specifies which frame this is in the series of frames within a video stream
    id = None
    # raw_frame is the actual ndarray
    raw_frame = None
    creation_timestamp = None
    service_timestamp = None
    completion_timestamp = None

    # Regular constructor
    def __init__(self, id_slot):
        # id_slot is going to be the same as frame_slot id
        self.id_slot = id_slot
        
    
    def copy_attributes(self, frame_obj):
        
        self.id = frame_obj.id
        self.raw_frame = frame_obj.raw_frame
        self.creation_timestamp = frame_obj.creation_timestamp
        self.service_timestamp = frame_obj.service_timestamp
        self.completion_timestamp = frame_obj.completion_timestamp

