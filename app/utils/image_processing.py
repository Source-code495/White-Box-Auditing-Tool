import torch
from PIL import Image
import torchvision.transforms as transforms
from werkzeug.utils import secure_filename
import os

def process_images(image_paths):
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    tensors = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    for path in image_paths:
        image = Image.open(path).convert('RGB')
        tensor = preprocess(image).unsqueeze(0).to(device)
        tensors.append(tensor)
    return tensors

def load_model(model_path):
    """Load a PyTorch model from file."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    try:
        model = torch.load(
            model_path,
            map_location=device
        )
        model.eval()
        return model
    except Exception as e:
        raise Exception(f"Failed to load model: {str(e)}")