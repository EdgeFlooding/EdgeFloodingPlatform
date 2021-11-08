import psutil
import threading
import time
import logging


def track_utilization(run_event, logger):
  while run_event.is_set():
    logger.info(f"CPU percentage: {psutil.cpu_percent(interval=2)}")
    logger.info(f"Memory percentage: {psutil.virtual_memory().percent}")


def main():

  # logging configuration
  LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
  logging.basicConfig(filename="test.log", level=logging.DEBUG, format=LOG_FORMAT, filemode="w")
  logger = logging.getLogger()

  # Event to terminate threads with ctrl + C
  run_event = threading.Event()
  run_event.set()

  # Preparing thread
  logger_thread = threading.Thread(target = track_utilization, args = (run_event, logger))

  logger_thread.start()

  try:
    while 1:
      time.sleep(.1)
  except KeyboardInterrupt:
    print("\nattempting to close threads")
    run_event.clear()

    # Waiting for thread to close

    logger_thread.join()
    print("threads successfully closed")


if __name__ == '__main__':
  main()
