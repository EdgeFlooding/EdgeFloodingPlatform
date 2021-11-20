from logging import log
import grpc
from concurrent import futures
import time
import json
import sys
import logging

# import the generated classes
import grpc_services_pb2
import grpc_services_pb2_grpc


def logger_setup(log_file):
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # logger configuration
    LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format=LOG_FORMAT, filemode="w")
    return logging.getLogger()


def encode_result(result):
    # to make it serializable
    for i, v in enumerate(result['detection_class_entities']):
        result['detection_class_entities'][i] = v.encode('utf-8')

    for i, v in enumerate(result['detection_class_names']):
        result['detection_class_names'][i] = v.encode('utf-8')
    
    return result


# based on .proto service
class AggregateResultServicer(grpc_services_pb2_grpc.ResultProcedureServicer):

    def __init__(self, logger):
        self.logger = logger


    def AggregateResult(self, request, context):
        response = grpc_services_pb2.Empty()
      
        id_node = request.id_node
        id_frame = request.id_frame
        id_camera = request.id_camera
        result = encode_result(json.loads(request.result_dict))
        num_bytes = request.ByteSize()
        #print(result)
        print("I received something...")
        self.logger.info(f"[RECEIVE] Node: {id_node}, Frame: {id_frame}, Camera: {id_camera}, Bytes: {num_bytes}")
        print("=======================")

        return response


def start_server(logger):
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))


    # add the defined class to the server
    grpc_services_pb2_grpc.add_ResultProcedureServicer_to_server(
            AggregateResultServicer(logger), server)

    # listen on port 5005
    print('Starting server. Listening on port 5004.')
    server.add_insecure_port('[::]:5004')
    server.start()
    return server


def main():

    if len(sys.argv) != 2:
        exit("Exiting...\nPlease provide the name of the log file")

    log_name = sys.argv[1]
    logger = logger_setup(log_name)

    server = start_server(logger)

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()