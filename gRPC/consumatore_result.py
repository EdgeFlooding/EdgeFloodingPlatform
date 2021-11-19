import grpc
from concurrent import futures
import time


# import the generated classes
import grpc_services_pb2
import grpc_services_pb2_grpc


import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
import tensorflow as tf

import numpy as np 
import base64


# based on .proto service
class AggregateResultServicer(grpc_services_pb2_grpc.ResultProcedureServicer):

    def AggregateResult(self, request, context):
        response = grpc_services_pb2.Empty()
      
        print("Ho ricevuto qualcosa")
        time.sleep(5)
        print(request.result_dict)
        print("Numero Bytes:", request.ByteSize())
        print("=======================")

        return response


def start_server():
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))


    # add the defined class to the server
    grpc_services_pb2_grpc.add_ResultProcedureServicer_to_server(
            AggregateResultServicer(), server)

    # listen on port 5005
    print('Starting server. Listening on port 5004.')
    server.add_insecure_port('[::]:5004')
    server.start()
    return server

if __name__ == '__main__':
    server = start_server()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)