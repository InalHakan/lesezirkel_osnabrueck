/**
 * File Size Validator for Django Admin
 * Validates file size before upload to prevent 413 errors
 */

(function() {
    'use strict';
    
    // Maximum file size in bytes (10 MB)
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB
    
    // Format bytes to human readable format
    function formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
    
    // Show error message
    function showError(input, message) {
        // Remove existing error messages
        const existingError = input.parentElement.querySelector('.file-size-error');
        if (existingError) {
            existingError.remove();
        }
        
        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'file-size-error';
        errorDiv.style.cssText = 'color: #ba2121; background-color: #fff0f0; border: 1px solid #ba2121; padding: 10px; margin-top: 10px; border-radius: 4px;';
        errorDiv.innerHTML = `
            <strong>⚠️ Datei zu groß!</strong><br>
            ${message}
        `;
        
        input.parentElement.appendChild(errorDiv);
    }
    
    // Clear error message
    function clearError(input) {
        const existingError = input.parentElement.querySelector('.file-size-error');
        if (existingError) {
            existingError.remove();
        }
    }
    
    // Validate file size
    function validateFileSize(input) {
        if (!input.files || input.files.length === 0) {
            clearError(input);
            return true;
        }
        
        const file = input.files[0];
        const fileSize = file.size;
        const fileName = file.name;
        
        if (fileSize > MAX_FILE_SIZE) {
            const message = `
                Die Datei <strong>"${fileName}"</strong> ist zu groß.<br>
                <strong>Dateigröße:</strong> ${formatBytes(fileSize)}<br>
                <strong>Maximum erlaubt:</strong> ${formatBytes(MAX_FILE_SIZE)}<br><br>
                <strong>Bitte:</strong><br>
                1. Komprimieren Sie das Bild mit <a href="https://tinypng.com/" target="_blank" style="color: #447e9b;">TinyPNG</a> oder <a href="https://squoosh.app/" target="_blank" style="color: #447e9b;">Squoosh</a><br>
                2. Oder wählen Sie eine kleinere Datei
            `;
            
            showError(input, message);
            
            // Clear the input
            input.value = '';
            
            // Show browser alert
            alert(
                `⚠️ Datei zu groß!\n\n` +
                `Datei: ${fileName}\n` +
                `Größe: ${formatBytes(fileSize)}\n` +
                `Maximum: ${formatBytes(MAX_FILE_SIZE)}\n\n` +
                `Bitte komprimieren Sie die Datei oder wählen Sie eine kleinere Datei.\n\n` +
                `Empfohlene Tools:\n` +
                `• TinyPNG: https://tinypng.com/\n` +
                `• Squoosh: https://squoosh.app/`
            );
            
            return false;
        }
        
        clearError(input);
        return true;
    }
    
    // Initialize validation on page load
    function initFileValidation() {
        // Find all file input fields
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        fileInputs.forEach(function(input) {
            // Add change event listener
            input.addEventListener('change', function() {
                validateFileSize(this);
            });
            
            // Add visual indicator
            const helpText = input.parentElement.querySelector('.help');
            if (helpText) {
                helpText.innerHTML += ` <strong style="color: #447e9b;">Max. ${formatBytes(MAX_FILE_SIZE)}</strong>`;
            } else {
                const hint = document.createElement('p');
                hint.className = 'help';
                hint.innerHTML = `Maximale Dateigröße: <strong style="color: #447e9b;">${formatBytes(MAX_FILE_SIZE)}</strong>`;
                input.parentElement.appendChild(hint);
            }
        });
    }
    
    // Validate before form submission
    function validateFormSubmission(event) {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        let hasError = false;
        
        fileInputs.forEach(function(input) {
            if (!validateFileSize(input)) {
                hasError = true;
            }
        });
        
        if (hasError) {
            event.preventDefault();
            
            // Scroll to first error
            const firstError = document.querySelector('.file-size-error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            
            alert('Bitte korrigieren Sie die Fehler bei den Dateiuploads.');
            return false;
        }
        
        return true;
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initFileValidation();
            
            // Add form submission validation
            const forms = document.querySelectorAll('form');
            forms.forEach(function(form) {
                form.addEventListener('submit', validateFormSubmission);
            });
        });
    } else {
        initFileValidation();
        
        // Add form submission validation
        const forms = document.querySelectorAll('form');
        forms.forEach(function(form) {
            form.addEventListener('submit', validateFormSubmission);
        });
    }
})();
