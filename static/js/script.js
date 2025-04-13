// CleanSheet JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            const alert = new bootstrap.Alert(message);
            alert.close();
        }, 5000);
    });

    // File input styling - show selected filename
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0]?.name || 'No file chosen';
            const fileLabel = this.nextElementSibling;
            if (fileLabel) {
                fileLabel.textContent = fileName;
            }
        });
    }

    // Enable tooltips everywhere
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});