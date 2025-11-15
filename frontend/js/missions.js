// Mission-related JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const createMissionForm = document.getElementById('createMissionForm');
    const categorySelect = document.getElementById('category');
    const difficultyGroup = document.getElementById('difficulty-group');
    const difficultySelect = document.getElementById('difficulty');

    // Show/hide difficulty field based on category
    if (categorySelect && difficultyGroup) {
        categorySelect.addEventListener('change', function() {
            if (this.value === 'Help/Favor') {
                difficultyGroup.style.display = 'block';
                difficultySelect.setAttribute('required', 'required');
            } else {
                difficultyGroup.style.display = 'none';
                difficultySelect.removeAttribute('required');
                difficultySelect.value = '';
            }
        });
    }

    // Create mission form validation
    if (createMissionForm) {
        createMissionForm.addEventListener('submit', function(e) {
            const title = document.getElementById('title').value;
            const description = document.getElementById('description').value;
            const category = document.getElementById('category').value;
            const difficulty = document.getElementById('difficulty').value;

            if (!title || !description || !category) {
                e.preventDefault();
                alert('Please fill in all required fields.');
                return false;
            }

            // Validate difficulty for Help/Favor category
            if (category === 'Help/Favor' && !difficulty) {
                e.preventDefault();
                alert('Please select a difficulty level for Help/Favor missions.');
                return false;
            }

            // File size validation
            const attachmentInput = document.getElementById('attachment');
            if (attachmentInput && attachmentInput.files.length > 0) {
                const file = attachmentInput.files[0];
                const maxSize = 16 * 1024 * 1024; // 16MB
                
                if (file.size > maxSize) {
                    e.preventDefault();
                    alert('File size must be less than 16MB.');
                    return false;
                }
            }
        });
    }

    // Mission acceptance confirmation
    const acceptForms = document.querySelectorAll('form[action*="/accept"]');
    acceptForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to accept this mission?')) {
                e.preventDefault();
            }
        });
    });

    // Mission completion confirmation
    const completeForms = document.querySelectorAll('form[action*="/complete"]');
    completeForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Mark this mission as completed? You will earn points.')) {
                e.preventDefault();
            }
        });
    });
});
