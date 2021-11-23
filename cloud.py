from logging import log
import grpc
from concurrent import futures
import time
import json
import sys
import logging
import threading
import requests

# import the generated classes
import grpc_services_pb2
import grpc_services_pb2_grpc


def current_time_int():
    return int(round(time.time() * 1000_000_000))


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


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    bearer_token = "AAAAAAAAAAAAAAAAAAAAACpyWAEAAAAAZdivw%2FpWKUtBaK0xIZVZ045Z%2B0Q%3DrIexy1px1FiNoo3HPlyDhHnEcHXdMG976MXlLgulGEDe1gPw6b"

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def update_tweets(run_event, lock, n_seconds):
    # UMBC Flood Bot id
    bot_id = 1173295284874596358
    url = "https://api.twitter.com/2/users/{}/tweets".format(bot_id)

    params = {"tweet.fields": "created_at"}

    while run_event.is_set():

        json_response = connect_to_endpoint(url, params)
        print(json.dumps(json_response, indent=4, sort_keys=True))

        # check if the json_response is changed or not

        # update it if necessary remember lock.acquire()!!!

        time.sleep(n_seconds)


    


# based on .proto service
class AggregateResultServicer(grpc_services_pb2_grpc.ResultProcedureServicer):

    def __init__(self, logger):
        self.logger = logger


    def AggregateResult(self, request, context):
        start_ts = current_time_int()
        response = grpc_services_pb2.Empty()
      
        id_node = request.id_node
        id_frame = request.id_frame
        id_camera = request.id_camera
        result = json.loads(request.result_dict)
        num_bytes = request.ByteSize()
        #print(result)
        print("I received something...")
        self.logger.info(f"[RECEIVE] Node: {id_node}, Frame: {id_frame}, Camera: {id_camera}, Bytes: {num_bytes}")
        print("=======================")

        dict_to_save = {'detection_class_entities': result['detection_class_entities'], 'detection_scores': result['detection_scores']}
        self.logger.info(f"[AGGREGATION]: {dict_to_save}")

        end_ts = current_time_int()
        self.logger.info(f"[AGG_LATENCY] Time: {end_ts-start_ts}")
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

    run_event = threading.Event()
    run_event.set()

    # Hard coded because we have a limit on the number of request we can issue to the twitter endpoint
    n_seconds = 60 

    lock = threading.Lock()
    twitter_thread = threading.Thread(target = update_tweets, args = (run_event, lock, n_seconds))
    twitter_thread.start()


    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)
        twitter_thread.join()


if __name__ == '__main__':
    main()