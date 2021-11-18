import grpc
from concurrent import futures
import time


# import the generated classes
import handle_new_frame_pb2
import handle_new_frame_pb2_grpc

import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
import tensorflow as tf

import numpy as np 
import base64

# For downloading the image.
import matplotlib.pyplot as plt


def save_image(image, image_name):
    Image.fromarray(image).save(image_name)


def resize_image(raw_frame, new_width, new_height):

    pil_image = Image.fromarray(np.uint8(raw_frame))
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")

    img = tf.convert_to_tensor(pil_image_rgb, dtype=tf.uint8)
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]

    return converted_img


def B64_to_numpy_array(b64img_compressed, w, h):
    b64decoded = base64.b64decode(b64img_compressed)

    decompressed = b64decoded #zlib.decompress(b64decoded)

    return np.frombuffer(decompressed, dtype=np.uint8).reshape(h, w, -1)

# based on .proto service
class FrameProcedureServicer(handle_new_frame_pb2_grpc.FrameProcedureServicer):

    def HandleNewFrame(self, request, context):
        response = handle_new_frame_pb2.Empty()
        '''
        print("New Frame received")
        print("id:", request.id)
        print("id_slot:", request.id_slot)
        print("width:", request.width)
        print("height", request.height)
        print("cr_tmp", request.creation_timestamp)
        raw_frame = B64_to_numpy_array(request.b64image, request.width, request.height)
        img = resize_image(raw_frame, 1280, 856)
        save_image(raw_frame, "prova.jpg")
        '''
        print(request.ByteSize())

        print("=======================")

        return response


def start_server():
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))


    # add the defined class to the server
    handle_new_frame_pb2_grpc.add_FrameProcedureServicer_to_server(
            FrameProcedureServicer(), server)

    # listen on port 5005
    print('Starting server. Listening on port 5005.')
    server.add_insecure_port('[::]:5005')
    server.start()
    return server

if __name__ == '__main__':
    server = start_server()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)