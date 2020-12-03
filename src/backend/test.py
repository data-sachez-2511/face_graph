import cv2
from json import loads, dumps
from manage import Manage


def test():
    manage_ = Manage()
    path = r'/mnt/c/Users/Xiaomi/Pictures/1.jpg'
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    label = 101
    meta = dumps({'name': 'sanek'})
    manage_.add(image=image, label=label, meta=meta)
    print(manage_.query(image=image, k=1))

if __name__ == '__main__':
    test()