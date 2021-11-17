
from PIL.Image import NONE


class Frame():

    # id specifies which frame this is in the series of frames within a video stream
    id = None
    id_slot = None
    # raw_frame is the actual ndarray
    raw_frame = None
    creation_timestamp = None
    service_timestamp = None
    completion_timestamp = None

    def __init__(self, id = None, id_slot = None, raw_frame = None, creation_timestamp = None):
        self.id = id
        # id_slot is going to be the same as frame_slot id
        self.id_slot = id_slot
        self.raw_frame = raw_frame
        self.creation_timestamp = creation_timestamp
        self.service_timestamp = None
        self.completion_timestamp = None

    def copy_attributes(self, frame_obj):

        self.id = frame_obj.id
        self.id_slot = frame_obj.id_slot
        self.raw_frame = frame_obj.raw_frame
        self.creation_timestamp = frame_obj.creation_timestamp
        self.service_timestamp = frame_obj.service_timestamp
        self.completion_timestamp = frame_obj.completion_timestamp

