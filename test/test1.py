
import time


t0 = time.clock()
t1 = time.time()
time.sleep(2.5)
interval1 = time.clock()
t2 = time.time()
interval2 = t2 - t1



print('t0:', t0)
print('t1:', t1)
print('t2:', t2)
print('interval1:', interval1)
print('interval2:', interval2)



