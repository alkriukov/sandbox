from threading import Thread
import time

def reach(name):
    print(f'Trying to reach {name}')
    time.sleep(len(name))
    print(f'Reached {name}')

my_family = ['Nika', 'Maxim', 'Vladislav', 'Olga', 'Alexey']
reach_threads = []
for name in my_family:
    name_thread = Thread(target=reach, args=(name,))
    reach_threads.append(name_thread)
    name_thread.start()

for t in reach_threads:
    t.join()
