# For running inference on the TF-Hub module.
import tensorflow as tf
import tensorflow_hub as hub

import grpc
from concurrent import futures
# import the generated classes
import handle_new_frame_pb2
import handle_new_frame_pb2_grpc
import base64

# For downloading the image.
import matplotlib.pyplot as plt

# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from frame_slot import FrameSlot
from frame import Frame
import time
import threading
import sys
import psutil
import logging

'''
This script waits for cameras to connect and insert each frame that arrives in the proper FrameSlot
There is also another thread that consumes frames with RR extraction and another thread to track the CPU and Memory utilization
Input: number of cameras that will connect to it, name of the log file to produce, the period of measures of utilization [s]
Output: log file with all the relevant info for statistical analysis, sends inference result to cloud
'''

'''
TODO:
        1) Send result to cloud
'''

def track_utilization(run_event, logger, seconds):
    '''Used by the logger_thread to write utilization data on log file'''
    while run_event.is_set():
        #print("Starting track utilization")
        logger.info(f"[UTILIZATION] CPU percentage: {psutil.cpu_percent(interval=seconds)}")
        logger.info(f"[UTILIZATION] Memory percentage: {psutil.virtual_memory().percent}")


def check_int(int_str):

    try:
        int(int_str)

    except ValueError:
        print("{} not an int!".format(int_str))
        return False

    return True


def logger_setup(log_file):
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # logger configuration
    LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format=LOG_FORMAT, filemode="w")
    return logging.getLogger()


def resize_image(raw_frame, new_width, new_height):
    '''Transform frame into tensor for detector'''
    pil_image = Image.fromarray(np.uint8(raw_frame))
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")

    img = tf.convert_to_tensor(pil_image_rgb, dtype=tf.uint8)
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

    return converted_img


def load_model_on_GPU(detector):
    '''To be called before actually using the detector on real frames'''

    img = np.zeros([856, 1280], np.uint8)
    img = resize_image(img, 1280, 856)
    run_detector(detector, img, setup = True)
    print("The model is ready")


def run_detector(detector, img, setup = False):
    '''if setup == True -> we are in the empty call, so no print required'''

    start_time = time.time()
    result = detector(img)
    end_time = time.time()

    if setup is False:
        print("Found %d objects." % len(result["detection_scores"]))
        print("Inference time: ", end_time-start_time)

        
        result = {key:value.numpy() for key,value in result.items()}
        
        return result


def round_robin_consume(fs_list, start_index):
    '''Returns the frame and the next index from which to start the next round_robin_consume'''

    fs_list_len = len(fs_list)

    current_index = start_index
    while True:
        frame_object = fs_list[current_index].consume_frame()
        #print(f"[RRC] Trying to extract Frame slot with index {current_index}")

        if frame_object == None:
            #print("Frame slot", str(fs_list[current_index].id) , "was empty")
            current_index = (current_index + 1) % fs_list_len

            if current_index == start_index: # All slots are empty
                return None, 0

            continue
        
        #print(f"Extracted frame {frame_object.id} from FrameSlot: {frame_object.id_slot}") # DEBUG
        return frame_object, (current_index + 1) % fs_list_len


def consume(detector, fs_list, run_event, logger):
    print("Consuming...")

    fs_index = 0

    while run_event.is_set():

        frame_object, fs_index = round_robin_consume(fs_list, fs_index)

        if frame_object == None:
            print("All frame slots were empty")
            time.sleep(1) # DEBUG
            continue

        img = resize_image(frame_object.raw_frame, 1280, 856)
        result = run_detector(detector, img)

        # Attention: the frames analysed are not saved anywhere!
        frame_object.completion_timestamp = time.time()

        #print("Analysed Frame with id: ", str(frame_object.id), "coming from frame slot: ", str(frame_object.id_slot))
        logger.info(f"[INFERENCE] ID: {frame_object.id} FRAMESLOT: {frame_object.id_slot} CREATION_TS: {frame_object.creation_timestamp} SERVICE_TS: {frame_object.service_timestamp} COMPLETION_TS: {frame_object.completion_timestamp}")

        # TODO SEND RESULT TO CLOUD
        

# ===================  gRPC SERVER FUNCTIONS ======================= #
def B64_to_numpy_array(b64img_compressed, w, h):
    b64decoded = base64.b64decode(b64img_compressed)

    decompressed = b64decoded #zlib.decompress(b64decoded)

    return np.frombuffer(decompressed, dtype=np.uint8).reshape(h, w, -1)


class FrameProcedureServicer(handle_new_frame_pb2_grpc.FrameProcedureServicer):

    def __init__(self, fs_list, logger):
        self.fs_list = fs_list
        self.logger = logger

    def HandleNewFrame(self, request, context):

        byte_size = request.ByteSize()
        id = request.id
        id_slot = request.id_slot
        width = request.width
        height = request.height
        creation_timestamp = request.creation_timestamp

        '''
        print("New Frame received")
        print("id:", id)
        print("id_slot:", id_slot)
        print("width:", width)
        print("height", height)
        print("cr_tmp", creation_timestamp)
        '''
        # Decode raw_frame
        raw_frame = B64_to_numpy_array(request.b64image, width, height)

        response = handle_new_frame_pb2.Empty()

        # check the slot id with size of fs_list
        if id_slot not in range(1, len(self.fs_list) + 1):
            print(f"[ERROR] id_slot: {id_slot} does not exist!")
            return response

        # create Frame to update the Frame Slot
        new_frame = Frame(id, id_slot, raw_frame, creation_timestamp)

        # update Frame Slot
        self.fs_list[id_slot - 1].update_frame(new_frame)

        # DEBUG PRINT
        #print(f"[DEBUG] inserted Frame with id: {id} in frame slot: {id_slot}")
        #print("=======================")

        self.logger.info(f"[BYTES] Received Frame {id} in slot {id_slot} with BYTES: {byte_size}")

        return response


def start_server(fs_list, logger):
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))


    # add the defined class to the server
    handle_new_frame_pb2_grpc.add_FrameProcedureServicer_to_server(
            FrameProcedureServicer(fs_list, logger), server)

    # listen on port 5005
    print('Starting server. Listening on port 5005.')
    server.add_insecure_port('[::]:5005')
    server.start()

    return server

# =================== END OF gRPC SERVER FUNCTIONS ===================== #


def main():

    # Check arguments
    n_arguments = len(sys.argv)
    if n_arguments != 4:
        exit("The number of argument is not correct\nPlease provide: number of cameras expected to connect, the name of the log file and the period of measures of utilization [s]")

    if not check_int(sys.argv[1]) and not check_int(sys.argv[3]): # we are just gonna trust the name of the log file
        exit()

    n_cameras = int(sys.argv[1])
    log_file = sys.argv[2]
    n_seconds = int(sys.argv[3])
    print("Arguments are OK")

    # Check available GPU devices.
    print("The following GPU devices are available: %s" % tf.test.gpu_device_name())

    # Get the detector
    module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
    detector = hub.load(module_handle).signatures['default']

    # Prepare the frameslot list
    fs_list = [FrameSlot(id) for id in range(1,n_cameras + 1)]

    logger = logger_setup(log_file)

    # Event to terminate threads with ctrl + C
    run_event = threading.Event()
    run_event.set()

    # Preparing threads
    logger_thread = threading.Thread(target = track_utilization, args = (run_event, logger, n_seconds))
    consumer_thread = threading.Thread(target = consume, args = (detector, fs_list, run_event, logger))

    # Load the detector on the GPU via a call on an empty tensor
    load_model_on_GPU(detector)

    logger_thread.start()
    time.sleep(.5)
    consumer_thread.start()
    server = start_server(fs_list, logger)

    try:
        while 1:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nattempting to close threads")
        server.stop(0)
        run_event.clear()

        # Waiting for threads to close
        consumer_thread.join()
        logger_thread.join()
        
        print("threads successfully closed")



if __name__ == '__main__':
    main()
