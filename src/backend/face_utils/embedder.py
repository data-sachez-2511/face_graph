import os
from pathlib import Path
import torch
from torchvision import transforms

class Embedder:
    def __init__(self):
        file_path = os.path.dirname(Path(__file__).absolute())
        self.model = torch.jit.load(os.path.join(file_path, 'ghostnet.pth'), map_location='cpu').eval()
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])

    def __call__(self, faces):
        inputs = [self.transform(face) for face in faces]
        with torch.no_grad():
            embeds = self.model(torch.stack(inputs)).numpy()
        return embeds