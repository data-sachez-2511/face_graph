import os
import numpy as np
import hnswlib
from joblib import dump, load

from .config import cfg


class HNSW:
    def __init__(self):
        self.path = cfg.hnsw_path
        self.index = hnswlib.Index(space='ip', dim=cfg.dim)
        if os.path.isfile(self.path):
            self.index.load_index(self.path, max_elements=cfg.max_elements)
            self.index.set_ef(cfg.ef_construction)
            self.map_labels = load(cfg.labels_path)
        else:
            self.index.init_index(max_elements=cfg.max_elements, ef_construction=cfg.ef_construction, M=cfg.M)
            self.map_labels = {'map': {}, 'current_size': 0}

    def add(self, vecs, label=None):
        if len(vecs.shape) == 1:
            vecs = np.array([vecs])
        norms = np.repeat(np.linalg.norm(vecs, axis=1).reshape((len(vecs), 1)), 512, axis=1)
        vecs = vecs / norms
        if self.index.get_current_count() == 0:
            if vecs.shape[0] == 1:
                self.add_(vecs[0], label)
                return [], "Success"
            else:
                return [], "Don\'t find connected persons, you should add one face for one user_id."
        k = min(self.map_labels['current_size'], cfg.max_channels)
        labels_q, distances_q = self.index.knn_query(vecs, k=k)
        if vecs.shape[0] == 1:
            if distances_q[0][0] <= cfg.threshold:
                return [], "You try add similar face in database."
            else:
                self.add_(vecs[0], label)
                return [], "Success"
        finded_users = set()
        for vec_id in range(vecs.shape[0]):
            for j in range(distances_q[vec_id].shape[0]):
                if distances_q[vec_id][j] < cfg.threshold:
                    finded_users.add(self.map_labels['map'][labels_q[vec_id][j]])
                else:
                    break
        result = {user: [] for user in finded_users}
        for user in result:
            result[user] = [_ for _ in finded_users if _ != user]
        return result, "Add connected persons."

    def add_(self, vec, label):
        internal_label = self.map_labels['current_size']
        self.map_labels['map'][internal_label] = label
        self.index.add_items([vec], [internal_label])
        self.map_labels['current_size'] += 1

    def query(self, vecs, k=1):
        k = min(k, self.index.get_current_count())
        norms = np.repeat(np.linalg.norm(vecs, axis=1).reshape((len(vecs), 1)), 512, axis=1)
        vecs = vecs / norms
        labels, dists = self.index.knn_query(vecs, k=k)
        for i in range(len(labels)):
            for j in range(len(labels[i])):
                labels[i][j] = self.map_labels['map'][labels[i][j]]
        return labels, dists

    def save(self):
        self.index.save_index(self.path)
        dump(self.map_labels, cfg.labels_path)
