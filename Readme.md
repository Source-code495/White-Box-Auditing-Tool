# White Box Auditing Tool

This platform allows you to upload images and perform adversarial attacks to observe their impact on deep learning model predictions. You can visualize how adversarial perturbations affect model confidence scores and cause misclassifications.

## Features

- **Image Upload**: Upload your own images for adversarial testing
- **Multiple Attack Methods**: Supports several adversarial attack techniques
- **Visual Comparison**: Side-by-side comparison of original and adversarial images
- **Confidence Analysis**: Track confidence score drops across different attack parameters
- **Class Change Detection**: Visualize how adversarial attacks cause misclassifications
- **Interactive Reports**: Generate detailed reports on model vulnerability

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- PyTorch and torchvision
- CUDA-compatible GPU (recommended for faster processing)

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the required environment variables:
   ```
   SECRET_KEY=your_secret_key
   UPLOAD_FOLDER=uploads
   # Add other configuration variables as needed
   ```

### Usage

1. Run the application:
   ```bash
   python run.py
   ```

2. Access the web interface at `http://localhost:5001`

3. Upload an image to analyze

4. Select an attack method and configure parameters

5. View the results showing how adversarial perturbations affect model predictions

## Attack Methods

The platform supports various adversarial attack techniques:

- **Fast Gradient Sign Method (FGSM)**: Quick single-step attack
- **Projected Gradient Descent (PGD)**: Iterative attack with higher success rate
- **DeepFool**: Minimal perturbation attack for misclassification
- **Carlini & Wagner (C&W)**: Optimization-based attack for targeted misclassification

## Project Structure

```
├── app/
│   ├── routes/           # URL endpoints
│   ├── services/         # Core attack implementation
│   ├── static/           # CSS, JS, images
│   ├── templates/        # HTML templates
│   ├── utils/            # Helper functions
│   └── __init__.py       # App initialization
├── uploads/              # Storage for uploaded files
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── run.py                # Entry point
```

