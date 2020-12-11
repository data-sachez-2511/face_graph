import os
from pathlib import Path

import torch
import numpy as np

from .layers.functions.prior_box import PriorBox
from .utils.box_utils import decode, decode_landm
from .utils.nms.py_cpu_nms import py_cpu_nms

import onnxruntime as ort


def preprocess(image):
    img = np.float32(image)

    im_height, im_width, _ = img.shape
    scale = torch.Tensor([im_width, im_height, im_width, im_height])
    img -= (104, 117, 123)
    img = img.transpose(2, 0, 1)
    img = torch.from_numpy(img).unsqueeze(0)
    img = img
    scale = scale
    return img.numpy(), scale


def postprocess(loc, conf, landms, scale, image_size, cfg):
    priorbox = PriorBox(cfg, image_size=image_size)
    priors = priorbox.forward()
    prior_data = priors.data
    boxes = decode(loc.data.squeeze(0), prior_data, cfg['variance'])
    boxes = boxes * scale
    boxes = boxes.cpu().numpy()
    scores = conf.squeeze(0).data.cpu().numpy()[:, 1]
    landms = decode_landm(landms.data.squeeze(0), prior_data, cfg['variance'])
    scale1 = torch.Tensor([image_size[1], image_size[0], image_size[1], image_size[0],
                           image_size[1], image_size[0], image_size[1], image_size[0],
                           image_size[1], image_size[0]])
    scale1 = scale1
    landms = landms * scale1
    landms = landms.cpu().numpy()

    # ignore low scores
    inds = np.where(scores > cfg.confidence_threshold)[0]
    boxes = boxes[inds]
    landms = landms[inds]
    scores = scores[inds]

    # keep top-K before NMS
    order = scores.argsort()[::-1][:cfg.top_k]
    boxes = boxes[order]
    landms = landms[order]
    scores = scores[order]

    # do NMS
    dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
    keep = py_cpu_nms(dets, cfg.nms_threshold)
    # keep = nms(dets, args.nms_threshold,force_cpu=args.cpu)
    dets = dets[keep, :]
    landms = landms[keep]

    # keep top-K faster NMS
    dets = dets[:cfg.keep_top_k, :]
    landms = landms[:cfg.keep_top_k, :]

    dets = np.concatenate((dets, landms), axis=1)
    return dets

class Detector:
    def __init__(self, cfg):
        self.cfg = cfg
        file_path = os.path.dirname(Path(__file__).absolute())
        self.model = ort.InferenceSession(os.path.join(file_path, 'retina_mnet.onnx'))

    def __call__(self, image):
        h, w, _ = image.shape
        input, scale = preprocess(image)
        input = {'input': input}
        loc, conf, landms = self.model.run(None, input)
        dets = postprocess(torch.from_numpy(loc), torch.from_numpy(conf), torch.from_numpy(landms), scale, (h, w),
                           self.cfg)
        return dets
