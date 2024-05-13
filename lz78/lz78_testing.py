"""
LZ78 testing
"""

from lz78.lz78 import LZ78
import random
import time

lst = [i for i in range(1000, 10)]
lst1 = []

for i in lst:
    time1 = time.time()
    time2 = time.time() - time1

    lst.append(time2)
