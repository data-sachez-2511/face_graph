import numpy as np

from .embedder import Embedder
from .detector import Detector
from .align.insightface import align_face
from .config import cfg_mnet as cfg
import cv2

MAX_BATCH_SIZE = 32


class FacePipe:
    def __init__(self):
        self.cfg = cfg
        self.detector = Detector(cfg)
        self.embedder = Embedder()

    def __call__(self, image, with_detect=False):
        if with_detect:
            dets = self.detector(image)
            faces = [align_face(image, det[5:]) for det in dets]
            embeds = self.embedder([cv2.cvtColor(_, cv2.COLOR_BGR2RGB) for _ in faces])
            return faces, embeds
        else:
            return self.embedder([cv2.cvtColor(image, cv2.COLOR_BGR2RGB)])
