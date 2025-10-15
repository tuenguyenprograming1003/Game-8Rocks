import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dls import dls_target

n = 8

def ids_target(tg, max_depth=n*2):
    for limit in range(max_depth):
        path = dls_target(tg, limit)
        if path:
            return path
    return []
