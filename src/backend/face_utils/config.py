import os
import torch
from easydict import EasyDict


# ================================Retina MobilenetV1 config=========================================
cfg_mnet = EasyDict()
cfg_mnet.min_sizes = [[16, 32], [64, 128], [256, 512]]
cfg_mnet.steps = [8, 16, 32]
cfg_mnet.variance = [0.1, 0.2]
cfg_mnet.clip = False
cfg_mnet.loc_weight = 2.0
cfg_mnet.gpu_train = True
cfg_mnet.batch_size = 32
cfg_mnet.ngpu = 1
cfg_mnet.epoch = 250
cfg_mnet.decay1 = 190
cfg_mnet.decay2 = 220
cfg_mnet.image_size = 640
cfg_mnet.pretrained = True
cfg_mnet.weight_path = os.path.join('weights', 'retina_mnet.pth')
cfg_mnet.return_layers = {'stage1': 1, 'stage2': 2, 'stage3': 3}
cfg_mnet.in_channel = 32
cfg_mnet.out_channel = 64
cfg_mnet.dsize = (300, 300, 3)
cfg_mnet.confidence_threshold = 0.6
cfg_mnet.top_k = 5000
cfg_mnet.nms_threshold = 0.4
cfg_mnet.keep_top_k = 750
cfg_mnet.mean_tensor = torch.tensor((104, 117, 123)).unsqueeze(0).unsqueeze(0)
# ================================Retina Resnet50 config=========================================

cfg_re50 = EasyDict()
cfg_re50.min_sizes = [[16, 32], [64, 128], [256, 512]]
cfg_re50.steps = [8, 16, 32]
cfg_re50.variance = [0.1, 0.2]
cfg_re50.clip = False
cfg_re50.loc_weight = 2.0
cfg_re50.gpu_train = True
cfg_re50.batch_size = 24
cfg_re50.ngpu = 4
cfg_re50.epoch = 100
cfg_re50.decay1 = 70
cfg_re50.decay2 = 90
cfg_re50.image_size = 840
cfg_re50.pretrained = True
cfg_re50.weight_path = os.path.join('weights', 'retina_r50.pth')
cfg_re50.return_layers = {'layer2': 1, 'layer3': 2, 'layer4': 3}
cfg_re50.in_channel = 256
cfg_re50.out_channel = 256
cfg_re50.dsize = (300, 300, 3)
cfg_re50.confidence_threshold = 0.5
cfg_re50.top_k = 5000
cfg_re50.nms_threshold = 0.4
cfg_re50.keep_top_k = 750
cfg_re50.mean_tensor = torch.tensor((104, 117, 123)).unsqueeze(0).unsqueeze(0)

