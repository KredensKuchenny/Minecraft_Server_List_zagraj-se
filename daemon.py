import time, threading
from functions.functions import list_updater, servers_updater

if __name__ == "__main__":
    background_thread_1 = threading.Thread(target=list_updater, daemon=True)
    background_thread_2 = threading.Thread(target=servers_updater, daemon=True)

    background_thread_1.start()
    background_thread_2.start()

    while True:
        time.sleep(60)
