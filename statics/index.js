// Mobile menu
const toggle = document.getElementById("menu-toggle");
const nav = document.getElementById("nav-links");

if (toggle && nav) {
    toggle.onclick = () => {
        if(nav.style.display === "flex"){
            nav.style.display = "none";
        } else {
            nav.style.display = "flex";
        }
    };
}

// Smooth scroll for hash links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e){
        const targetAttr = this.getAttribute("href");
        if (targetAttr === "#") return;
        
        const target = document.querySelector(targetAttr);
        if(target) {
            e.preventDefault();
            target.scrollIntoView({
                behavior:"smooth"
            });
            // Close mobile menu if open
            if(nav && nav.style.display === "flex") {
                nav.style.display = "none";
            }
        }
    });
});

// Scroll animation for sections
const sections = document.querySelectorAll("section");
function reveal(){
    const triggerBottom = window.innerHeight * 0.85;
    sections.forEach(section => {
        const boxTop = section.getBoundingClientRect().top;
        if(boxTop < triggerBottom){
            section.style.opacity = "1";
            section.style.transform = "translateY(0)";
        }
    });
}
window.addEventListener("scroll", reveal);
reveal();

// File upload preview & drag/drop UI handling
function handleFileInput(inputId, previewContainerId, previewElementId) {
    const fileInput = document.getElementById(inputId);
    const dropArea = fileInput ? fileInput.closest('.file-drop-area') : null;
    const previewContainer = document.getElementById(previewContainerId);
    const previewElement = document.getElementById(previewElementId);
    const fileNameDisplay = document.getElementById(inputId + '-name');

    if (!fileInput || !dropArea) return;

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.remove('dragover'), false);
    });

    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length > 0) {
            fileInput.files = files; // Assign files to the input
            handleFiles(files);
        }
    }

    // Handle selected files via click
    fileInput.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            handleFiles(this.files);
        }
    });

    function handleFiles(files) {
        if (files.length === 0) return;
        const file = files[0];
        
        // Display file name
        if (fileNameDisplay) {
            fileNameDisplay.textContent = file.name;
        }

        // Display preview
        if (previewContainer && previewElement) {
            const fileURL = URL.createObjectURL(file);
            previewElement.src = fileURL;
            previewContainer.style.display = 'block';
            
            // Clean up memory
            if (previewElement.tagName.toLowerCase() === 'img') {
                previewElement.onload = function() {
                    URL.revokeObjectURL(previewElement.src);
                }
            }
        }
    }
}

// Form submission spinner
function handleFormSubmit(formId, btnId) {
    const form = document.getElementById(formId);
    const btn = document.getElementById(btnId);
    
    if (!form || !btn) return;

    form.addEventListener('submit', function(e) {
        // Show spinner if form is valid
        if (form.checkValidity()) {
            const spinner = btn.querySelector('.spinner');
            const btnText = btn.querySelector('.btn-text');
            const btnIcon = btn.querySelector('.btn-icon');
            
            btn.disabled = true;
            if (spinner) spinner.style.display = 'inline-block';
            if (btnIcon) btnIcon.style.display = 'none';
            if (btnText) btnText.textContent = 'Processing...';
        }
    });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    handleFileInput('image-input', 'image-preview-container', 'image-preview');
    handleFileInput('audio-input', 'audio-preview-container', 'audio-preview');
    handleFormSubmit('detect-form', 'submit-btn');
});