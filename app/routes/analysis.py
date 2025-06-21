from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.services.attack_service import perform_attack_analysis
from app.utils.file_handling import (
    valid_model_file,
    create_session,
    save_model,
    save_uploaded_files
)
from app.utils.image_processing import load_model, process_images
from app.utils.stats import get_class_stats
from app.utils.visualization import generate_visualizations
from app.utils.gemini_integration import generate_analysis_report

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/upload', methods=['POST'])
def handle_file_upload():
    # Get selected attacks and parameters
    selected_attacks = request.form.getlist('attacks')
    attack_params = {
        'FGSM': {'eps': float(request.form.get('fgsm_eps', 0.1))},
        'PGD': {
            'eps': float(request.form.get('pgd_eps', 0.1)),
            'eps_step': float(request.form.get('pgd_step', 0.01)),
            'max_iter': int(request.form.get('pgd_iters', 40))
        },
        'CW': {
            'confidence': float(request.form.get('cw_confidence', 0.0)),
            'learning_rate': float(request.form.get('cw_lr', 0.01)),
            'max_iter': int(request.form.get('cw_iters', 10))
        },
        'UAP': {
            'delta': float(request.form.get('uap_delta', 0.2)),
            'max_iter': int(request.form.get('uap_iters', 20))
        }
    }

    # Validate at least one attack selected
    if not selected_attacks:
        flash('Please select at least one attack method!', 'error')
        return redirect(url_for('main.index'))

    # File validation
    if 'model' not in request.files:
        flash('No model file uploaded', 'error')
        return redirect(url_for('main.index'))

    model_file = request.files['model']
    if not valid_model_file(model_file):
        flash('Invalid model file', 'error')
        return redirect(url_for('main.index'))

    # Create session
    session_id, session_dir = create_session()
    
    try:
        # Save and load model
        model_path = save_model(model_file, session_dir)
        model = load_model(model_path)
        
        # Process images
        image_paths, filenames = save_uploaded_files(
            request.files.getlist('images'), 
            session_dir
        )
        image_tensors = process_images(image_paths)

        # Perform attack analysis for each selected method
        all_results = {}
        all_class_stats = {}
        all_analysis = {}
        
        for attack_name in selected_attacks:
            # Get parameters for current attack
            params = attack_params.get(attack_name, {})
            
            # Perform attack-specific analysis
            results = perform_attack_analysis(
                model=model,
                image_tensors=image_tensors,
                session_dir=session_dir,
                filenames=filenames,
                attack_name=attack_name,
                attack_params=params
            )
            
            # Store results
            all_results[attack_name] = results
            all_class_stats[attack_name] = get_class_stats(results)
            all_analysis[attack_name] = generate_analysis_report(
                all_class_stats[attack_name]
            )

        return render_template('analysis/results.html',
            session_id=session_id,
            attacks=selected_attacks,
            all_results=all_results,
            all_class_stats=all_class_stats,
            all_plots={attack: generate_visualizations(results, session_dir) 
                      for attack, results in all_results.items()},
            gemini_analysis=all_analysis
        )
        
    except Exception as e:
        import traceback
        error_message = f'Processing error: {str(e)}'
        print(error_message)
        print(traceback.format_exc())
        flash(error_message, 'error')
        return redirect(url_for('main.index'))