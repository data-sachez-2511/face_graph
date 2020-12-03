import os
from pathlib import Path

from easydict import EasyDict

cfg = EasyDict()
file_path = os.path.dirname(Path(__file__).absolute().parent)

cfg.hnsw_path = os.path.join(file_path, 'data', 'index.hnsw')

cfg.db_path = os.path.join(file_path, 'data', 'meta.db')

cfg.dim = 512
cfg.max_elements = 2 ** 14
cfg.ef_construction = 200
cfg.M = 16
cfg.hard = True
cfg.threshold = 0.5
cfg.max_channels = 10
