from random import randint
import config as cfg


def create_file():
    with open(cfg.FILE_NAME, 'w') as f:
        for i in range(cfg.CNT_TEST):
            x = randint(cfg.MIN_X, cfg.MAX_X)
            y = randint(cfg.MIN_Y, cfg.MAX_Y)
            f.write(f'{x} {y}\n')


def read_file() -> [int, int]:
    with open(cfg.FILE_NAME) as f:
        data = list(map(lambda line: tuple(map(int, line.split())), f.readlines()))
    return data
