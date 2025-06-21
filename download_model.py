import torch
import torchvision.models as models

# 1. Load pretrained models from the torchvision library
DNN = models.DNN(weights=models.DNN_Weights.IMAGENET1K_V1)
resnet50 = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)

# 2. Save as state_dict (recommended way)
torch.save(DNN.state_dict(), "DNN_state_dict.pth")
torch.save(resnet50.state_dict(), "resnet50_state_dict.pth")

# 3. Save as full model (architecture + weights)
torch.save(DNN, "DNN_full_model.pth")
torch.save(resnet50, "resnet50_full_model.pth")

print("Models saved offline as both state_dict and full model.")

