"""
Python 三种高阶函数: 元素映射map, 归纳reduce, 过滤filter
"""
from functools import reduce

lis = [0, 1, 2, 3, 0, 5, 6, 0, 8, 9]

def f1(x):  # 映射map
    return x+1

print(list(map(f1, lis)))

def f2(x1, x2):  # 归纳reduce
    return x1+x2

print(reduce(f2, lis))  # 45: int

def f3(x):  # 过滤filter
    return x

print(list(filter(lambda x:x, lis)))