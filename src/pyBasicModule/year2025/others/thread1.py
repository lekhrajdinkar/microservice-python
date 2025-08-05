import threading
import time

def print_numbers():
    for i in range(5):
        print(f"🧵 Inner Thread: step {i} out of {5} done ")
        time.sleep(1)
    print("child thread finished")

t = threading.Thread(target=print_numbers)
t.start()

print("💻 Main thread continues...")
print("💻 Main thread ... need to wait to child for child thread "); t.join()
#print("💻 Main thread ... need to wait to child for child thread , max= 10 sec"); t.join(timeout=10)
print("✅ Main Thread completed.")
