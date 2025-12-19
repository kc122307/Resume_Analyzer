// Resume upload functionality
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('resume-upload');
    const fileLabel = fileInput ? fileInput.nextElementSibling : null;
    
    if (fileInput && fileLabel) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                fileLabel.textContent = fileName;
                fileLabel.classList.add('bg-green-600');
                fileLabel.classList.remove('bg-blue-600');
            }
        });
    }
});