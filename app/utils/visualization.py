import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import os

def generate_visualizations(results, session_dir):
    # Calculate metrics
    total = len(results)
    success = sum(1 for r in results if r['original_pred'] != r['adv_pred'])
    success_rate = success / total * 100
    confidences = [r['adv_confidence'] for r in results]
    
    # Create figures
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    
    # Success rate pie chart
    labels = ['Successful Attacks', 'Failed Attacks']
    sizes = [success_rate, 100-success_rate]
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    ax1.set_title('Attack Success Rate')
    
    # Confidence distribution
    ax2.hist(confidences, bins=20, range=(0,1))
    ax2.set_xlabel('Adversarial Prediction Confidence')
    ax2.set_ylabel('Count')
    ax2.set_title('Confidence Distribution')
    
    # Class change matrix
    class_changes = {}
    for r in results:
        key = (r['original_class'], r['adv_class'])
        class_changes[key] = class_changes.get(key, 0) + 1
    
    classes = sorted(set([r['original_class'] for r in results] + 
                      [r['adv_class'] for r in results]))
    matrix = np.zeros((len(classes), len(classes)))
    
    for (orig, adv), count in class_changes.items():
        i = classes.index(orig)
        j = classes.index(adv)
        matrix[i,j] = count
    
    im = ax3.imshow(matrix, cmap='viridis')
    ax3.set_xticks(np.arange(len(classes)))
    ax3.set_yticks(np.arange(len(classes)))
    ax3.set_xticklabels(classes, rotation=90)
    ax3.set_yticklabels(classes)
    ax3.set_xlabel('Adversarial Class')
    ax3.set_ylabel('Original Class')
    fig3.colorbar(im, ax=ax3)
    
    # Save plots
    plot_paths = {}
    for fig, name in zip([fig1, fig2, fig3], ['pie', 'hist', 'matrix']):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plot_data = base64.b64encode(buf.read()).decode('ascii')
        plot_paths[name] = f"data:image/png;base64,{plot_data}"
        plt.close(fig)
    
    return plot_paths
