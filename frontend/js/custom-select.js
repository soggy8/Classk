// Custom dropdown select component for Classk design system

document.addEventListener('DOMContentLoaded', function() {
    // Initialize custom dropdowns
    initCustomSelects();
});

function initCustomSelects() {
    // Wait a bit to ensure DOM is fully ready, especially for dynamically shown elements
    setTimeout(function() {
        const selectElements = document.querySelectorAll('.custom-select-wrapper select');
        
        selectElements.forEach(function(select) {
            // Check if custom select is already initialized
            if (select.parentElement && select.parentElement.classList.contains('custom-select-wrapper') && select.parentElement.querySelector('.custom-select-trigger')) {
                return; // Already initialized
            }
            createCustomSelect(select);
        });
    }, 100);
}

// Re-initialize function for dynamically shown elements
function reinitCustomSelects() {
    const selectElements = document.querySelectorAll('.custom-select-wrapper select');
    
    selectElements.forEach(function(select) {
        // Check if custom select is already initialized
        const wrapper = select.parentElement;
        if (wrapper && wrapper.classList.contains('custom-select-wrapper') && wrapper.querySelector('.custom-select-trigger')) {
            return; // Already initialized
        }
        
        // Create custom select for this element
        createCustomSelect(select);
    });
    
    // Also check for selects that might not have the wrapper yet
    const allSelects = document.querySelectorAll('select');
    allSelects.forEach(function(select) {
        if (select.parentElement && select.parentElement.classList.contains('custom-select-wrapper')) {
            // Has wrapper, check if initialized
            if (!select.parentElement.querySelector('.custom-select-trigger')) {
                createCustomSelect(select);
            }
        }
    });
}

function createCustomSelect(selectElement) {
    // Get existing wrapper if select is inside one
    let wrapper = selectElement.parentElement;
    
    // Check if already initialized
    if (wrapper && wrapper.classList.contains('custom-select-wrapper') && wrapper.querySelector('.custom-select-trigger')) {
        return; // Already initialized
    }
    
    // If no wrapper exists, create one
    if (!wrapper || !wrapper.classList.contains('custom-select-wrapper')) {
        wrapper = document.createElement('div');
        wrapper.className = 'custom-select-wrapper';
        wrapper.dataset.value = selectElement.value;
        selectElement.parentNode.insertBefore(wrapper, selectElement);
        wrapper.appendChild(selectElement);
    } else {
        wrapper.dataset.value = selectElement.value;
    }
    
    // Create the display button
    const selectedText = document.createElement('div');
    selectedText.className = 'custom-select-trigger';
    // Get first non-empty option or use placeholder
    const currentValue = selectElement.value;
    if (currentValue === '' || !currentValue) {
        selectedText.textContent = selectElement.options[0]?.text || 'Select category';
    } else {
        selectedText.textContent = selectElement.options[selectElement.selectedIndex]?.text || 'Select category';
    }
    
    // Create dropdown menu
    const dropdown = document.createElement('div');
    dropdown.className = 'custom-select-dropdown';
    dropdown.style.display = 'none';
    
    // Create options (skip placeholder/empty options and currently selected option)
    Array.from(selectElement.options).forEach(function(option, index) {
        // Skip empty/placeholder options in the dropdown
        if (option.value === '') {
            return;
        }
        
        // Skip currently selected option (it's already shown in the trigger)
        if (option.value === selectElement.value) {
            return;
        }
        
        const optionDiv = document.createElement('div');
        optionDiv.className = 'custom-select-option';
        optionDiv.textContent = option.text;
        optionDiv.dataset.value = option.value;
        
        optionDiv.addEventListener('click', function() {
            selectElement.value = option.value;
            wrapper.dataset.value = option.value;
            selectedText.textContent = option.text;
            
            // Rebuild dropdown options to show the previously selected option
            // and hide the newly selected one
            rebuildDropdownOptions();
            
            // Trigger change event
            selectElement.dispatchEvent(new Event('change', { bubbles: true }));
            
            // Close dropdown
            wrapper.classList.remove('open');
            setTimeout(function() {
                if (!wrapper.classList.contains('open')) {
                    dropdown.style.display = 'none';
                }
            }, 300);
        });
        
        dropdown.appendChild(optionDiv);
    });
    
    // Function to rebuild dropdown options when selection changes
    function rebuildDropdownOptions() {
        // Clear current options
        dropdown.innerHTML = '';
        
        // Rebuild options excluding the newly selected one
        Array.from(selectElement.options).forEach(function(option) {
            // Skip empty/placeholder options
            if (option.value === '') {
                return;
            }
            
            // Skip currently selected option
            if (option.value === selectElement.value) {
                return;
            }
            
            const optionDiv = document.createElement('div');
            optionDiv.className = 'custom-select-option';
            optionDiv.textContent = option.text;
            optionDiv.dataset.value = option.value;
            
            optionDiv.addEventListener('click', function() {
                selectElement.value = option.value;
                wrapper.dataset.value = option.value;
                selectedText.textContent = option.text;
                
                // Rebuild again
                rebuildDropdownOptions();
                
                // Trigger change event
                selectElement.dispatchEvent(new Event('change', { bubbles: true }));
                
                // Close dropdown
                dropdown.style.display = 'none';
                wrapper.classList.remove('open');
            });
            
            dropdown.appendChild(optionDiv);
        });
    }
    
    // Toggle dropdown
    selectedText.addEventListener('click', function(e) {
        e.stopPropagation();
        const isOpen = wrapper.classList.contains('open');
        
        // Close all other dropdowns
        document.querySelectorAll('.custom-select-wrapper').forEach(function(w) {
            w.classList.remove('open');
            setTimeout(function() {
                if (!w.classList.contains('open')) {
                    const dd = w.querySelector('.custom-select-dropdown');
                    if (dd) {
                        dd.style.display = 'none';
                    }
                }
            }, 300);
        });
        
        if (!isOpen) {
            // Rebuild dropdown options to ensure currently selected is excluded
            rebuildDropdownOptions();
            
            // Calculate actual height needed
            dropdown.style.display = 'block';
            dropdown.style.maxHeight = 'none';
            dropdown.style.opacity = '0';
            dropdown.style.visibility = 'visible';
            
            // Force reflow to measure
            void dropdown.offsetHeight;
            
            const actualHeight = dropdown.scrollHeight;
            // Set a maximum height (300px) with scroll, but use actual height if smaller
            const maxDropdownHeight = Math.min(actualHeight, 300);
            dropdown.style.maxHeight = '0';
            
            // Set display to block
            wrapper.classList.add('open');
            
            // Set max-height to actual height for smooth animation
            setTimeout(function() {
                dropdown.style.maxHeight = maxDropdownHeight + 'px';
                dropdown.style.opacity = '1';
            }, 10);
        } else {
            wrapper.classList.remove('open');
            dropdown.style.maxHeight = '0';
            dropdown.style.opacity = '0';
            // Wait for transition to finish before hiding
            setTimeout(function() {
                if (!wrapper.classList.contains('open')) {
                    dropdown.style.display = 'none';
                    dropdown.style.visibility = 'hidden';
                }
            }, 300);
        }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!wrapper.contains(e.target)) {
            wrapper.classList.remove('open');
            setTimeout(function() {
                if (!wrapper.classList.contains('open')) {
                    dropdown.style.display = 'none';
                }
            }, 300);
        }
    });
    
    // Insert custom elements (they don't exist yet)
    selectElement.style.display = 'none';
    wrapper.insertBefore(selectedText, selectElement);
    wrapper.insertBefore(dropdown, selectElement);
    
    // Listen to programmatic changes
    selectElement.addEventListener('change', function() {
        const selectedOption = selectElement.options[selectElement.selectedIndex];
        // If empty value selected, show placeholder text
        if (selectElement.value === '' || !selectedOption) {
            selectedText.textContent = selectElement.options[0]?.text || 'Select category';
        } else {
            selectedText.textContent = selectedOption.text;
        }
        wrapper.dataset.value = selectElement.value;
        
        // Rebuild dropdown to hide the newly selected option
        rebuildDropdownOptions();
    });
}

// Make functions available globally for use in other scripts
window.reinitCustomSelects = reinitCustomSelects;
window.createCustomSelect = createCustomSelect;

