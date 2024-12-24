function showError(message, errorElementId, cond=false) {
    var existingError = document.querySelector('.error-message:not([style*="display: none"])')

    if (existingError) {
        return;
    }

    var errorElement = document.getElementById(errorElementId)

    if (errorElement) {
        errorElement.innerText = message
        
        errorElement.style.display = 'block'
        if (cond) {
            errorElement.style.marginBottom = '-14px'
        } else {
            errorElement.style.marginBottom = '-17px'
        }

    }
}


function hideError() {
    var errorElements = document.querySelectorAll('.error-message')

    errorElements.forEach((errorElement) => {
        errorElement.style.display = 'none';
    });
}
