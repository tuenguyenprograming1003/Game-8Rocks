import random

n = 8

def tao_mau():
    """Tạo bàn cờ mẫu ngẫu nhiên"""
    cols = list(range(n))
    random.shuffle(cols)
    return cols

__all__ = ['n', 'tao_mau']
