import os
from pathlib import Path

import torch
import numpy as np

from .layers.functions.prior_box import PriorBox
from .utils.box_utils import decode_batch, decode_landm_batch
from .utils.nms.py_cpu_nms import py_cpu_nms

from .utils_ import rescale_images, add_padding


def preprocess(images, cfg):
    images_, scales = rescale_images(images, cfg.dsize)
    images_ = add_padding(images_, cfg.dsize)
    images_ = torch.from_numpy(images_).float()
    scales = torch.from_numpy(scales)
    images_ -= cfg.mean_tensor
    images_ = images_.permute(0, 3, 1, 2)
    return images_, scales


def get_prior(cfg):
    priorbox = PriorBox(cfg, image_size=(cfg.model_size, cfg.model_size))
    priors = priorbox.forward()
    return priors.data


def postprocess(tensor, scales, cfg):
    loc, conf, landms = tensor[:, :, :4], tensor[:, :, 4:6], tensor[:, :, 6:]
    boxes = decode_batch(loc, cfg.prior_data, cfg.variance)
    scale = torch.stack(
        [torch.Tensor([cfg.model_size, cfg.model_size, cfg.model_size, cfg.model_size]) for _ in scales])
    boxes = boxes * scale.unsqueeze_(-1).expand(boxes.shape[0], boxes.shape[2], boxes.shape[1]).transpose(1, 2) / \
            scales.unsqueeze_(-1).expand(boxes.shape[0], boxes.shape[1] * boxes.shape[2]).view(boxes.shape[0],
                                                                                               boxes.shape[1],
                                                                                               boxes.shape[2])
    scores = conf[:, :, 1]
    landms = decode_landm_batch(landms, cfg.prior_data, cfg.variance)
    scale1 = torch.stack([torch.Tensor([cfg.model_size, cfg.model_size, cfg.model_size, cfg.model_size,
                                        cfg.model_size, cfg.model_size, cfg.model_size, cfg.model_size,
                                        cfg.model_size, cfg.model_size]) for _ in scales])
    landms = landms * scale1.unsqueeze_(-1).expand(landms.shape[0], landms.shape[2], landms.shape[1]) \
        .transpose(1, 2) / scales.expand(landms.shape[0], landms.shape[1] * landms.shape[2]) \
                 .view(landms.shape[0], landms.shape[1], landms.shape[2])
    inds = [torch.nonzero(scores[i] > cfg.confidence_threshold, as_tuple=False).view(-1) for i in range(len(scores))]
    boxes = [boxes[i][inds[i]].numpy() for i in range(len(boxes))]
    landms = [landms[i][inds[i]].numpy() for i in range(len(landms))]
    scores = [scores[i][inds[i]].numpy() for i in range(len(scores))]
    order = [scores[i].argsort()[::-1][:cfg.top_k] for i in range(len(scores))]
    boxes = [boxes[i][order[i]] for i in range(len(boxes))]
    landms = [landms[i][order[i]] for i in range(len(landms))]
    scores = [scores[i][order[i]] for i in range(len(scores))]

    #         # do NMS
    dets = [np.hstack((boxes[i], scores[i][:, np.newaxis])).astype(np.float32, copy=False) for i in
            range(len(boxes))]
    keep = [py_cpu_nms(dets[i], cfg.nms_threshold) for i in range(len(dets))]
    #         keep = [nms(dets[i], args.nms_threshold,force_cpu=args.cpu) for i in range(tensors.shape[0])]
    dets = [dets[i][keep[i], :] for i in range(len(dets))]
    landms = [landms[i][keep[i]] for i in range(len(dets))]

    #         # keep top-K faster NMS
    dets = [dets[i][:cfg.keep_top_k, :] for i in range(len(dets))]
    landms = [landms[i][:cfg.keep_top_k, :] for i in range(len(landms))]

    dets = [np.concatenate((dets[i], landms[i]), axis=1) for i in range(len(dets))]
    return dets


class Detector:
    def __init__(self, cfg):
        self.cfg = cfg
        self.cfg.model_size = 300
        self.cfg.dsize = (300, 300, 3)
        self.cfg.prior_data = get_prior(cfg)
        file_path = os.path.dirname(Path(__file__).absolute())
        self.model = torch.jit.load(os.path.join(file_path, 'mobilenet_300.pth'), map_location='cpu').eval()

    def __call__(self, images):
        inputs, scales = preprocess(images, self.cfg)
        with torch.no_grad():
            outputs = self.model(inputs)
        dets = postprocess(outputs, scales, self.cfg)
        return dets
