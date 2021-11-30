import random
from config import config


def create_x():
    x = random.randint(config['MIN_X'], config['MAX_X'])
    return x


def create_y():
    y = random.randint(config["MIN_Y"], config['MAX_Y'])
    return y


def create_test_file():
    with open(config['FILE_NAME'], 'w') as f:
        f.write(str(config['CNT_TEST']) + '\n')
        for i in range(config['CNT_TEST']):
            x, y = create_x(), create_y()
            f.write(f'{x} {y}\n')


def main():
    create_test_file()


if __name__ == '__main__':
    main()
