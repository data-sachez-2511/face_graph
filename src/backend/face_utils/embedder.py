import os
from pathlib import Path
import torch
import onnxruntime as ort
from torchvision import transforms


class Embedder:
    def __init__(self):
        file_path = os.path.dirname(Path(__file__).absolute())
        self.model = ort.InferenceSession(os.path.join(file_path, 'attention92irse.onnx'))
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])

    def __call__(self, faces):
        inputs = [self.transform(face) for face in faces]
        inputs = torch.stack(inputs).numpy()
        with torch.no_grad():
            embeds = self.model.run(None, {'input': inputs})[0]
        return embeds
