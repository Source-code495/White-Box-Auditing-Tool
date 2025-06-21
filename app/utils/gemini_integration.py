import google.generativeai as genai
import json
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest')

def generate_analysis_report(class_stats):
    try:
        prompt = f"""**Security Analysis Report**

        **Precontext**
        1. Fast Gradient Sign Method (FGSM)
        Vulnerabilities Exposed:

        Gradient Reliance and Linear Components: FGSM exploits the linearity of DNN's decision boundaries by leveraging gradients of the loss function with respect to input data. The attack adds perturbations in the direction of the gradient sign, causing misclassification. This reveals DNN's susceptibility to simple gradient-based manipulations, particularly in its linear layers (e.g., fully connected layers) where perturbations amplify due to the model’s high-dimensional parameter space 315.

        Low Robustness to Single-Step Perturbations: FGSM demonstrates that even small, imperceptible perturbations (e.g., ε = 0.3) can drastically reduce DNN's accuracy by up to 25%, highlighting its lack of robustness to adversarial noise introduced in a single optimization step 615.

        2. Projected Gradient Descent (PGD)
        Vulnerabilities Exposed:

        Iterative Optimization of Non-Robust Features: PGD iteratively refines perturbations to maximize loss, exploiting DNN’s sensitivity to cumulative gradient updates. This reveals that the model’s feature representations are not robust to iterative adversarial training, as PGD can bypass defenses like adversarial training by finding local maxima in the loss landscape 3618.

        Over-Reliance on High-Frequency Features: PGD attacks often perturb high-frequency components in images (e.g., edges and textures), which DNN heavily relies on for classification. This indicates that the model’s hierarchical convolutional layers are vulnerable to perturbations that alter these critical features 618.

        Accuracy Reduction: In experiments, PGD reduced DNN’s accuracy by up to 67% in medical imaging tasks, underscoring its effectiveness against models trained on domain-specific data 3.

        3. Carlini & Wagner (CW) Attack
        Vulnerabilities Exposed:

        Optimization-Based Decision Boundary Exploitation: The CW attack formulates adversarial example generation as an optimization problem, minimizing perturbation size while ensuring misclassification. This reveals weaknesses in DNN’s decision boundaries, particularly its inability to resist perturbations that exploit the model’s confidence scores (logits) 618.

        Higher Success Rate: Compared to FGSM and PGD, CW caused a 35% accuracy drop in DNN, demonstrating its ability to craft perturbations that are both imperceptible and highly effective. This highlights DNN’s lack of robustness to sophisticated loss function manipulations 6.

        Bypassing Defenses: CW’s ability to circumvent defenses like gradient masking shows that DNN’s security mechanisms are insufficient against attacks targeting its loss landscape 18.

        4. Universal Adversarial Perturbations (UAP)
        Vulnerabilities Exposed:

        Linear Layer Susceptibility: UAPs exploit the ill-conditioned nature of DNN’s linear layers (e.g., fully connected layers) by aligning perturbations with the right singular vectors of weight matrices. This reveals that the model’s linear components act as "amplifiers" for adversarial noise, making it vulnerable to data-agnostic attacks 510.

        Transferability Across Models: UAPs generated for DNN can transfer to other architectures (e.g., ResNet, DenseNet), indicating that its vulnerabilities are partly rooted in shared architectural traits like linear operators and Lipschitz continuity properties 510.

        Efficiency in Black-Box Settings: Even with partial knowledge of DNN’s layers, UAPs achieve high attack success rates (e.g., ~4% drop with 50% layer access), highlighting its lack of robustness to attacks that exploit intrinsic model properties 5.

        Key Takeaways
        Architectural Weaknesses: DNN’s deep, linear-heavy architecture makes it prone to gradient-based and optimization-driven attacks.

        Feature Sensitivity: The model’s reliance on high-frequency and non-robust features allows adversaries to craft perturbations that exploit these dependencies.

        Defense Limitations: Current defense mechanisms (e.g., adversarial training) are insufficient against advanced attacks like CW and UAPs, necessitating hybrid approaches such as autoencoder-based denoising 3 or secondary verification with classical ML models 

        **Class Misclassification Statistics**
        {json.dumps(class_stats, indent=2)}
        **Required Analysis Format**
        1. ### Vulnerability Analysis
            - List top 3 classes with misclassification rates
            - Try to infer why certain classes are vulnerable in this kind of attack

        2. ### Defense Recommendations
            - Suggest defense recommendations for each types of attack
            - Suggest some other well known defense techniques

        Use proper Markdown formatting with code blocks, tables, and lists."""
        
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"## Analysis Error\n```python\n{str(e)}\n```"