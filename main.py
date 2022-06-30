"""
Big O n * log2(n)
Алгоритм Грэхема
"""
import data
import src
import config

if __name__ == '__main__':
    if not config.FILE:
        data.create_file()
    points = data.read_file()
    src.draw_algorithm_graham(points)
