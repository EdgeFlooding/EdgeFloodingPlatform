import grpc
from concurrent import futures
import time
import json


# import the generated classes
import grpc_services_pb2
import grpc_services_pb2_grpc


def encode_result(result):
    # to make it serializable
    for i, v in enumerate(result['detection_class_entities']):
        result['detection_class_entities'][i] = v.encode('utf-8')

    for i, v in enumerate(result['detection_class_names']):
        result['detection_class_names'][i] = v.encode('utf-8')
    
    return result


# based on .proto service
class AggregateResultServicer(grpc_services_pb2_grpc.ResultProcedureServicer):

    def AggregateResult(self, request, context):
        response = grpc_services_pb2.Empty()
      
        result = encode_result(json.loads(request.result_dict))
        print(result)
        print("Number of Bytes:", request.ByteSize())
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