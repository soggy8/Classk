// Mission-related JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const createMissionForm = document.getElementById('createMissionForm');
    const categorySelect = document.getElementById('category');
    const difficultyGroup = document.getElementById('difficulty-group');
    const difficultySelect = document.getElementById('difficulty');

    // Show/hide difficulty field based on category with smooth animation
    if (categorySelect && difficultyGroup) {
        categorySelect.addEventListener('change', function() {
            if (this.value === 'Help/Favor') {
                // Show difficulty field with animation
                difficultyGroup.style.display = 'block';
                difficultySelect.setAttribute('required', 'required');
                // Trigger animation
                setTimeout(function() {
                    difficultyGroup.classList.add('show');
                    // Re-initialize custom select for difficulty after it's fully visible
                    setTimeout(function() {
                        if (typeof reinitCustomSelects === 'function') {
                            reinitCustomSelects();
                        }
                        // Also try direct initialization for difficulty select
                        const difficultyWrapper = difficultySelect.parentElement;
                        if (difficultyWrapper && difficultyWrapper.classList.contains('custom-select-wrapper')) {
                            if (!difficultyWrapper.querySelector('.custom-select-trigger')) {
                                if (typeof createCustomSelect === 'function') {
                                    createCustomSelect(difficultySelect);
                                }
                            }
                        }
                    }, 350);
                }, 10);
            } else {
                // Hide difficulty field with animation
                difficultyGroup.classList.remove('show');
                difficultySelect.removeAttribute('required');
                difficultySelect.value = '';
                // Remove display after animation
                setTimeout(function() {
                    if (!difficultyGroup.classList.contains('show')) {
                        difficultyGroup.style.display = 'none';
                    }
                }, 300);
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
