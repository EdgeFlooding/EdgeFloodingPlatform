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


def synchronized(lock):
    """ Synchronization decorator. """

    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap


class Tweets():

    lock = threading.Lock()
    last_tweets = None
    time_for_request = 0

    @synchronized(lock)
    def update_last_tweets(self, new_tweets, new_time_required):
        self.last_tweets = new_tweets
        self.time_for_request = new_time_required

    @synchronized(lock)
    def get_last_tweets(self):
        return self.last_tweets, self.time_for_request



def current_time_int():
    return int(round(time.time() * 1000_000_000))


def logger_setup(log_file):
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # logger configuration
    LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
    logging.basicConfig(filename=log_file, level=logging.INFO, format=LOG_FORMAT, filemode="w")
    return logging.getLogger()


def encode_result(result):
    '''Convert the result dictionary to the original format'''
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
    '''Performs the GET request to the twitter endpoint'''
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def update_tweets(run_event, tweets_obj, n_seconds, logger):
    '''Periodically queries twitter to get the last tweets of UMBC Flood Bot and update the last_tweets'''
    # UMBC Flood Bot id
    bot_id = 1173295284874596358
    url = "https://api.twitter.com/2/users/{}/tweets".format(bot_id)

    params = {"tweet.fields": "created_at"}

    while not run_event.is_set():
        try:
            start_ts = current_time_int()
            json_response = connect_to_endpoint(url, params)
            end_ts = current_time_int()
        except Exception:
            print("Cannot retrieve json")
            logger.info("[TWITTER_ERROR]")
            run_event.wait(n_seconds)
            continue

        last_tweets, _ = tweets_obj.get_last_tweets()
        time_for_request = end_ts - start_ts
        # Mutual exclusion with server threads
        # check if last_tweets must be updated or not
        if last_tweets is None or last_tweets['meta']['newest_id'] != json_response['meta']['newest_id']:
            tweets_obj.update_last_tweets(json_response, time_for_request)
        else:
            tweets_obj.update_last_tweets(last_tweets, time_for_request)
        
        run_event.wait(n_seconds)


# based on .proto service
class AggregateResultServicer(grpc_services_pb2_grpc.ResultProcedureServicer):

    def __init__(self, logger, tweets_obj):
        self.logger = logger
        self.tweets_obj = tweets_obj


    def AggregateResult(self, request, context):
        start_ts = current_time_int()
        response = grpc_services_pb2.Empty()

        id_node = request.id_node
        id_frame = request.id_frame
        id_camera = request.id_camera
        result = json.loads(request.result_dict)
        num_bytes = request.ByteSize()

        print("I received something...")
        self.logger.info(f'[RECEIVE] {{"Edge_Node": {id_node}, "Frame": {id_frame}, "Camera": {id_camera}, "Bytes": {num_bytes}}}')
        print("=======================")

        # I only save a subset of the dictionary received
        if 'detection_class_entities' in result.keys(): # inception or mobilenet results
            dict_to_save = {'detection_class_entities': result['detection_class_entities'], 'detection_scores': result['detection_scores']}
        else: # yolov5 results
            dict_to_save = result 

        # Strings to search to find the actual float value of rain intensity
        rain_intensity = "Rain Intensity : "
        the_day = "The day is"
        # If rain intensity is above this value it is a strong signal for possible flooding
        threshold = 0.5
        
        last_tweets, time_for_tweets = self.tweets_obj.get_last_tweets()

        # The twitter_thread hasn't updated this value yet
        if last_tweets is None:
            dict_to_save['Flooding'] = False

        else:
            text = last_tweets['data'][0]['text'] # I only look at the last tweet
            rain_index = text.find(rain_intensity)
            end_index = text.find(the_day)
            if rain_index == -1 or end_index == -1: # Just in case the text has a different format
                dict_to_save['Flooding'] = False
            else:
                rain_intensity_float = float(text[rain_index + len(rain_intensity):end_index])
                dict_to_save['Flooding'] = rain_intensity_float > threshold 

        self.logger.info(f"[AGGREGATION]: {json.dumps(dict_to_save)}")

        end_ts = current_time_int()
        self.logger.info(f'[AGG_LATENCY] {{"Time": {end_ts - start_ts}, "Time_for_tweets": {time_for_tweets}}}')
        return response


def start_server(logger, tweets_obj):
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=12))


    # add the defined class to the server
    grpc_services_pb2_grpc.add_ResultProcedureServicer_to_server(
            AggregateResultServicer(logger, tweets_obj), server)

    # listen on port 5000
    print('Starting server. Listening on port 5000.')
    server.add_insecure_port('[::]:5000')
    server.start()
    return server


def main():

    if len(sys.argv) != 2:
        exit("Exiting...\nPlease provide the name of the log file")

    log_name = sys.argv[1]

    # Hard coded because we have a limit on the number of request we can issue to the twitter endpoint
    n_seconds = 90
    tweets_obj = Tweets()

    logger = logger_setup(log_name)
    server = start_server(logger, tweets_obj)

    run_event = threading.Event()
    twitter_thread = threading.Thread(target = update_tweets, args = (run_event, tweets_obj, n_seconds, logger))
    twitter_thread.start()


    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)
        run_event.set()
        twitter_thread.join()


if __name__ == '__main__':
    main()