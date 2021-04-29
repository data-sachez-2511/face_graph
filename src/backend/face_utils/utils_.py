import numpy as np
import cv2

PADDING_COLOR = (0, 0, 0)


def add_padding(images, dsize=(224, 224, 3)):
    """
    Add padding to images and stack to np.array
    :param images: List of images [List[np.array]]
    :param dsize: Destination images size (height, wight, channels) [Tuple[int]]
    :return: Numpy array of size: (len(images) X dsize[0] X dsize[1] X dsize[2]) [np.array]
    """
    result = np.full((len(images), dsize[0], dsize[1], dsize[2]), PADDING_COLOR, dtype=np.uint8)
    for i in range(len(images)):
        result[i, :images[i].shape[0], :images[i].shape[1], :] = images[i]
    return result


def rescale_images(images, dsize=(224, 224, 3)):
    """
    Resize (while maintaining scale) those images that do not fit into the array with size = dsize
    :param images: List of images [List[np.array]]
    :param dsize: Destination images size (height, wight, channels) [Tuple[int]]
    :return: List of rescaled images and scales [Tuple(List[np.array], np.array)]
    """
    #     bottleneck function
    resized_images = []
    scales = []
    for i in range(len(images)):
        ht, wd, cc = images[i].shape
        scale = 1
        if ht >= wd and ht > dsize[0]:
            scale = dsize[0] / ht
        elif ht < wd and wd > dsize[1]:
            scale = dsize[1] / wd
        if scale < 1:
            new_size = (int(wd * scale), int(ht * scale))
            resized_images.append(cv2.resize(images[i], new_size, interpolation=cv2.INTER_AREA))
            scales.append(scale)
        else:
            resized_images.append(images[i])
            scales.append(1.0)
    return resized_images, np.array(scales)


def draw_detections(image, dets, color=(255, 0, 0), thick=2):
    image_draw = image.copy()
    for det in dets:
        cv2.rectangle(image_draw, (int(det[0]), int(det[1])), (int(det[2]), int(det[3])), color, thick)
        cv2.putText(image_draw, '{:4f}'.format(det[4]), (int(det[0]), int(det[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    color, thick)
        points = [(int(det[5 + i]), int(det[5 + i + 1])) for i in range(0, 10, 2)]
        for point in points:
            image_draw = cv2.circle(image_draw, point, radius=1, color=color, thickness=4)
    return image_draw
