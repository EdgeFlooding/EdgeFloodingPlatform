
class Frame():

    def __init__(self, id):
        # id is going to be the same as frame_slot id
        self.id = id
        # raw_frame is the actual ndarray
        self.raw_frame = 0
        self.creation_timestamp = 0
        self.service_timestamp = 0

