import threading
import time

def esegui(e, t):
    while not e.is_set():
        print("Scrivo")
        e.wait(timeout=t)


e = threading.Event()
t = 0

th = threading.Thread(target = esegui, args = (e, t))

th.start()

try:
    while 1:
        time.sleep(5)
except KeyboardInterrupt:
    print("\nattempting to close threads")
    e.set()
    th.join()