import torch
import torchvision.transforms as transforms
import os
from PIL import Image
import numpy as np
from art.attacks.evasion import (
    FastGradientMethod,
    ProjectedGradientDescent,
    CarliniL2Method,
    UniversalPerturbation
)
from art.estimators.classification import PyTorchClassifier

# Load ImageNet labels
def load_imagenet_labels():
    url = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"
    import requests, json
    response = requests.get(url)
    class_idx = json.loads(response.text)
    return {int(k): v[1] for k, v in class_idx.items()}

idx2label = load_imagenet_labels()

def perform_attack_analysis(model, image_tensors, session_dir, filenames=None, attack_name="FGSM", attack_params=None):
    """
    Perform attack analysis on a list of images.
    
    Args:
        model: PyTorch model
        image_tensors: List of image tensors
        session_dir: Directory to save adversarial images
        filenames: List of original filenames
        attack_name: Type of attack to perform (FGSM, PGD, CW, UAP)
        attack_params: Dictionary of attack-specific parameters
        
    Returns:
        List of results
    """
    # Default parameters if none provided
    if attack_params is None:
        attack_params = {}
    
    # Get the device
    device = next(model.parameters()).device
    
    # Convert to ART-compatible format
    batch = torch.cat(image_tensors, dim=0)
    x_numpy = batch.cpu().detach().numpy()
    
    # Create ART classifier
    classifier = create_art_classifier(model)
    
    # Generate adversarial examples based on attack type
    if attack_name == "FGSM":
        attack = FastGradientMethod(
            classifier, 
            eps=attack_params.get('eps', 0.1),
            batch_size=batch.size(0)
        )
    elif attack_name == "PGD":
        attack = ProjectedGradientDescent(
            classifier,
            eps=attack_params.get('eps', 0.1),
            eps_step=attack_params.get('eps_step', 0.01),
            max_iter=attack_params.get('max_iter', 40),
            batch_size=batch.size(0)
        )
    elif attack_name == "CW":
        attack = CarliniL2Method(
            classifier,
            confidence=attack_params.get('confidence', 0.0),
            learning_rate=attack_params.get('learning_rate', 0.01),
            max_iter=attack_params.get('max_iter', 10),
            batch_size=batch.size(0)
        )
    elif attack_name == "UAP":
        attack = UniversalPerturbation(
            classifier,
            delta=attack_params.get('delta', 0.2),
            max_iter=attack_params.get('max_iter', 20),
            attacker="fgsm",  # Base attacker
            batch_size=batch.size(0)
        )
    else:
        raise ValueError(f"Unsupported attack type: {attack_name}")
    
    # Generate adversarial examples
    x_adv_numpy = attack.generate(x=x_numpy)
    
    # Get predictions and save results
    results = process_predictions(
        model=model,
        original_batch=batch,
        adversarial_batch=torch.from_numpy(x_adv_numpy).to(device),
        session_dir=session_dir,
        filenames=filenames,
        attack_name=attack_name
    )
    
    # Add attack metadata to results
    for result in results:
        result['attack_type'] = attack_name
        result['attack_params'] = attack_params
    
    return results

def create_art_classifier(model):
    return PyTorchClassifier(
        model=model,
        clip_values=(0.0, 1.0),
        loss=torch.nn.CrossEntropyLoss(),
        input_shape=(3, 224, 224),
        nb_classes=1000,
        device_type='cuda' if torch.cuda.is_available() else 'cpu'
    )

def process_predictions(model, original_batch, adversarial_batch, session_dir, filenames=None, attack_name="FGSM"):
    # Get the device
    device = next(model.parameters()).device
    
    # Prediction logic
    with torch.no_grad():
        orig_outputs = model(original_batch)
        adv_outputs = model(adversarial_batch)
    
    # Process results and save images
    return generate_results(
        orig_outputs=orig_outputs,
        adv_outputs=adv_outputs,
        adversarial_batch=adversarial_batch,
        session_dir=session_dir,
        filenames=filenames,
        attack_name=attack_name
    )

def generate_results(orig_outputs, adv_outputs, adversarial_batch, session_dir, filenames=None, attack_name="FGSM"):
    # Get predictions
    orig_probs = torch.softmax(orig_outputs, 1)
    adv_probs = torch.softmax(adv_outputs, 1)
    orig_conf, orig_preds = torch.max(orig_probs, 1)
    adv_conf, adv_preds = torch.max(adv_probs, 1)
    
    # Save adversarial images and collect results
    results = []
    
    # If filenames aren't provided, use generic names
    if filenames is None:
        filenames = [f"image_{i}.jpg" for i in range(adversarial_batch.size(0))]
    
    for i in range(adversarial_batch.size(0)):
        orig_class = idx2label[orig_preds[i].item()]
        adv_class = idx2label[adv_preds[i].item()]
        
        # Save adversarial image with attack type in filename
        adv_img = transforms.ToPILImage()(adversarial_batch[i].cpu())
        output_path = os.path.join(session_dir, f"{attack_name}_adv_{filenames[i]}")
        adv_img.save(output_path)
        
        results.append({
            'original': filenames[i],
            'adversarial': f"{attack_name}_adv_{filenames[i]}",
            'original_class': orig_class,
            'adv_class': adv_class,
            'original_confidence': orig_conf[i].item(),
            'adv_confidence': adv_conf[i].item(),
            'original_pred': orig_preds[i].item(),
            'adv_pred': adv_preds[i].item(),
            'is_successful': orig_preds[i].item() != adv_preds[i].item()
        })
    
    return results