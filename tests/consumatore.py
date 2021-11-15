import grpc
from concurrent import futures
import time


# import the generated classes
import handle_new_frame_pb2
import handle_new_frame_pb2_grpc


import numpy as np 
import base64
import zlib

def B64_to_numpy_array(b64img_compressed, w, h):
    b64decoded = base64.b64decode(b64img_compressed)

    decompressed = b64decoded #zlib.decompress(b64decoded)

    return np.frombuffer(decompressed, dtype=np.uint8).reshape(w, h, -1)

# based on .proto service
class FrameProcedureServicer(handle_new_frame_pb2_grpc.FrameProcedureServicer):

    def HandleNewFrame(self, request, context):
        response = handle_new_frame_pb2.Empty()
        print(request.id)
        print(request.id_slot)
        print(request.width)
        print(request.height)
        print(request.creation_timestamp)
        img = B64_to_numpy_array(request.b64image, request.width, request.height)
        print("Ho ricevuto un frame")

        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))


# add the defined class to the server
handle_new_frame_pb2_grpc.add_FrameProcedureServicer_to_server(
        FrameProcedureServicer(), server)

# listen on port 5005
print('Starting server. Listening on port 5005.')
server.add_insecure_port('[::]:5005')
server.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    server.stop(0)