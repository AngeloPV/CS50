function showError(message, errorElementId, margin_bottom) {
    var existingError = document.querySelector('.error-message:not([style*="display: none"])')

    if (existingError) {
        return;
    }

    var errorElement = document.getElementById(errorElementId)

    if (errorElement) {
        errorElement.innerText = message
        console.log(`-${margin_bottom}px`)    
        errorElement.style.display = 'block'
        errorElement.style.marginBottom = `-${margin_bottom}px` //margin_bottom
        // if (cond) {
        //     errorElement.style.marginBottom = '-14px'
        // } else {
        //     errorElement.style.marginBottom = '-10px'
        // }

    }
}


function hideError() {
    var errorElements = document.querySelectorAll('.error-message')

    errorElements.forEach((errorElement) => {
        errorElement.style.display = 'none';
    });
}
