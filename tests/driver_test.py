import threading
from frame_slot import FrameSlot
import random
import time

fs = FrameSlot(1)


def produce():

    i = 0

    while True:
        print("Produco Roba: " + str(i))
        fs.update_frame("Roba: " + str(i))
        i = i + 1

        if i == 10:
            print("Fine Produzione")
            break
        time.sleep(1)
    

def consume():
    
    i = 0

    while True:
        print("Consumo")
        frame = fs.consume_frame()

        i = i + 1

        if i == 20:
            print("Fine consumazione")
            break

        if frame == None:
            print("Lo slot era vuoto")
            continue

        print("Nome Frame: ", frame.raw_frame)
        time.sleep(random.randint(1, 4))
        


thread_prod = threading.Thread(name = "Producer", target = produce, daemon = True)
thread_consum = threading.Thread(name = "Consumer", target = consume, daemon = True)


thread_prod.start()
thread_consum.start()


thread_prod.join()
thread_consum.join()

