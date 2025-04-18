// Exibe um alerta personalizado para dar um feedback ao usuário
function showCustomAlert(classModal, title, htmlContent=null, icon, confirmButtonText, css) {
    // Cria um overlay para cobrir o conteúdo da página

    let overlay = document.createElement('div');
    overlay.className = 'custom-swal-overlay';
    document.body.appendChild(overlay);
    
    // Exibe o alerta usando a biblioteca SweetAlert2
    if (classModal == null) {
        Swal.fire({
            title: title,
            html: htmlContent,  
            icon: icon,  
            confirmButtonText: confirmButtonText,
            showCloseButton: true,
            heightAuto: false,
            backdrop: 'rgba(0, 0, 0, 0.5)',
            customClass: {
                popup: 'custom-swal-popup',
                container: 'custom-swal-container',
                title: css[0],
                confirmButton: css[1]
            }, 
            willClose: () => {
                document.body.removeChild(overlay);
            }
        })

        return
    }

    const formContainer = document.querySelector(classModal);

    // Inicialmente, o formulário pode estar escondido
    formContainer.classList.add('hide-form');

    // Exibe o alerta usando a biblioteca SweetAlert2
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
        // Remove o overlay quando o alerta for fechado
        willClose: () => {
            document.body.removeChild(overlay);
        }
    }).then((result) => { // Verifica se o alerta foi confirmado
        if (result.isConfirmed) { 
            document.querySelector('.form-container').classList.remove('hide-form');
            document.querySelector('.form-container').classList.add('show-form');
        }
    });
    
    // Adiciona um evento de clique no container do SweetAlert, fechando o alerta e exibindo o formulário

    Swal.getContainer().addEventListener('click', () => {
        document.querySelector('.form-container').classList.remove('hide-form');
        document.querySelector('.form-container').classList.add('show-form');
    });
}
