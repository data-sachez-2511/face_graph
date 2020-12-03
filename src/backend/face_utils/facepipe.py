import numpy as np

from .embedder import Embedder
from .detector import Detector
from .align.insightface import align_face
from .config import cfg_mnet as cfg

MAX_BATCH_SIZE = 32


class FacePipe:
    def __init__(self):
        self.cfg = cfg
        self.detector = Detector(cfg)
        self.embedder = Embedder()

    def __call__(self, images):
        dets = sum([self.detector(images[i: i + MAX_BATCH_SIZE]) for i in range(0, len(images), MAX_BATCH_SIZE)], [])
        faces = [[align_face(images[i], det[5:]) for det in dets[i]] for i in range(len(dets))]
        idx_map = {}
        faces_batch = []
        for i in range(len(faces)):
            for j in range(len(faces[i])):
                idx_map[len(idx_map)] = i
                faces_batch.append(faces[i][j])
        embeds = []
        for i in range(0, len(faces_batch), MAX_BATCH_SIZE):
            embeds.append(self.embedder(faces_batch[i:i + MAX_BATCH_SIZE]))
        embeds = np.concatenate(embeds)
        for i in range(len(embeds)):
            idx = idx_map[i]
            face = faces_batch[i]
            embed = embeds[i]
            yield idx, face, embed
