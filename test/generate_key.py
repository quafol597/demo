
import datetime

a = datetime.datetime.strptime('2021-01-23 10:00:00', '%Y-%m-%d %H:%M:%S')
b = datetime.datetime.strptime('2021-03-15 03:00:00', '%Y-%m-%d %H:%M:%S')
c = b-a
print(a)
print(b)
print(c)
print(50*24+12)