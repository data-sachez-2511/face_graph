import cv2

from json import dumps
from facepipe import FacePipe


def test():
    pipe = FacePipe()
    path = r'/mnt/c/Users/Xiaomi/Pictures/1.jpg'
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    print(dumps(list(pipe(images=[image]))))


if __name__ == '__main__':
    test()

