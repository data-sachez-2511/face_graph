import numpy as np
from random import randint

from hnsw import HNSW
from sqlite import ResultStorage, Face


def test():
    hnsw = HNSW()
    size = 200
    vecs = np.random.random(size * 512).reshape((size, 512))
    labels = np.random.randint(0, 100, size)
    print(len(hnsw.add(vecs=vecs[:size // 2], labels=labels[:size // 2])))
    print(hnsw.index.get_current_count())
    print(len(hnsw.add(vecs=vecs, labels=labels)))
    print(hnsw.index.get_current_count())

    print(len(hnsw.add(vecs=vecs, labels=labels)))
    print(hnsw.index.get_current_count())

    print('rights labels: {}'.format(labels[:5]))
    print('result query: {}'.format(hnsw.query(vecs[:5], k=3)))


if __name__ == '__main__':
    test()
