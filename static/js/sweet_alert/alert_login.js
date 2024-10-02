function showCustomAlert(title, htmlContent, icon, confirmButtonText, css) {
    const loginContainer = document.querySelector('.login-container');

    // Inicialmente, o formulário pode estar escondido
    loginContainer.classList.add('hide-form');

    let overlay = document.createElement('div');
    overlay.className = 'custom-swal-overlay';
    document.body.appendChild(overlay);

    Swal.fire({
        title: title,
        html: htmlContent,  // Permite que o conteúdo HTML seja renderizado
        icon: icon,  
        confirmButtonText: confirmButtonText,
        customClass: {
            popup: 'custom-swal-popup',
            container: 'custom-swal-container',
            title: css[0],
            confirmButton: css[1]
        }, 
        willClose: () => {
            document.body.removeChild(overlay);
        }
    }).then((result) => {
        if (result.isConfirmed) {
            document.querySelector('.login-container').classList.remove('hide-form');
            document.querySelector('.login-container').classList.add('show-form');
        }
    });

    Swal.getContainer().addEventListener('click', () => {
        document.querySelector('.login-container').classList.remove('hide-form');
        document.querySelector('.login-container').classList.add('show-form');
    });
}