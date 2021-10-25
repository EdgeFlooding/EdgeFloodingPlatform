
class Frame():

    def __init__(self, id):
        # id is going to be the same as frame_slot id
        self.id = id
        # raw_frame is the actual ndarray
        self.raw_frame = None
        self.creation_timestamp = None
        self.service_timestamp = None
        self.completion_timestamp = None

