import threading
import time

def esegui(e, t, s):
    while e.is_set():
        print("Scrivo")
        s.wait(timeout=t)


e = threading.Event()
e.set()
s = threading.Event()
t = 1

th = threading.Thread(target = esegui, args = (e, t, s))

th.start()

try:
    while 1:
        time.sleep(5)
except KeyboardInterrupt:
    print("\nattempting to close threads")
    e.clear()
    s.set()
    th.join()