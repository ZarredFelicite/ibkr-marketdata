import time
import threading

def child_function(param1, param2):
    print(str(param1 * param2))
    while True:
        print("doing some stuff")
        time.sleep(3)

def main_function():
    print("Initializing some things.")
    for _ in range(10):
        x = threading.Thread(target=child_function, args=(3,5, ))
        x.start()

main_function()