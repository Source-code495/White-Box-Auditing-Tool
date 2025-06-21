document.addEventListener('DOMContentLoaded', () => {
    const modelInput = document.getElementById('model');
    const imagesInput = document.getElementById('images');
    const form = document.getElementById('uploadForm');

    // Handle model file selection
    modelInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            document.getElementById('modelStatus').innerHTML = `
                <span class="text-success">
                    <i class="bi bi-check-circle"></i>
                    Selected: ${file.name}
                </span>
            `;
        }
    });

    // Handle image files selection
    imagesInput.addEventListener('change', (e) => {
        const files = e.target.files;
        if (files.length > 0) {
            document.getElementById('imageStatus').innerHTML = `
                <span class="text-success">
                    <i class="bi bi-check-circle"></i>
                    Selected ${files.length} image${files.length > 1 ? 's' : ''}
                </span>
            `;
        }
    });

    // Form validation
    form.addEventListener('submit', (e) => {
        let valid = true;
        
        if (!modelInput.files.length) {
            document.getElementById('modelStatus').innerHTML = `
                <span class="text-danger">
                    <i class="bi bi-exclamation-circle"></i>
                    Please select a model file
                </span>
            `;
            valid = false;
        }

        if (!imagesInput.files.length) {
            document.getElementById('imageStatus').innerHTML = `
                <span class="text-danger">
                    <i class="bi bi-exclamation-circle"></i>
                    Please select at least one image
                </span>
            `;
            valid = false;
        }

        if (!valid) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
});