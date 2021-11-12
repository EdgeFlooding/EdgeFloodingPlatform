import grpc

# import the generated classes
import handle_new_frame_pb2
import handle_new_frame_pb2_grpc

# data encoding

import numpy as np 
import base64
import zlib
import time

# open a gRPC channel
channel = grpc.insecure_channel('127.0.0.1:5005')

# create a stub (client)
stub = handle_new_frame_pb2_grpc.FrameProcedureStub(channel)

# encoding image/numpy array

t1 = time.time()
for _ in range(1000):
    frame = np.random.randint(0,255, (416,416,3), dtype=np.uint8) # dummy rgb image

    # compress

    # data = zlib.compress(frame)

    data = base64.b64encode(frame)

    # create a valid request message
    frame_req = handle_new_frame_pb2.Frame(id = 1, id_slot = 1,  b64image = data, width = 416, height = 416, creation_timestamp = time.time())

    # make the call
    response = stub.HandleNewFrame(frame_req)
    print("Frame sent")
    break
t2 = time.time()

print(t2-t1)
# printing response
# print(response.channel)
# print(response.mean)