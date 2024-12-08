//Redireciona o botão de logout
document.getElementById('logout').addEventListener('click', function() {
    window.location.href = "/logout";
});
//Redireciona o botão de deletar a conta
document.getElementById('delete_account').addEventListener('click', function() {
    let confirmation = confirm("Você realmente deseja excluir sua conta? Esta ação não pode ser desfeita.");

    if (confirmation) {
        // se o usuário confirmar, cria um formulário dinamicamente para enviar o POST
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = "/delete_account/index"; // Rota do Flask

        // Cria um input para enviar a confirmação
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'confirmation';
        input.value = 'yes';  // O valor 'yes' será enviado se o usuário confirmar
        form.appendChild(input);

        // Adiciona o formulário no body e faz o submit do form
        document.body.appendChild(form);
        form.submit();}
});

//Faz com que o card seja alterado após clicar no botão edit-btn do respectivo card, onde vai ficar uma
//borda em volta dos campos para o usuario poder selecionar e ao selecionar ele será redirecionado pra
//página de edição do campo na qual ele clicou

//Para o card 2
document.querySelectorAll('.card:nth-child(2) .edit_btn').forEach(button => {
let isEditMode = false;  

button.addEventListener('click', () => {
    if (!isEditMode) {
        document.querySelectorAll('.card:nth-child(2) .mid .subtitle').forEach(item => {
            item.style.fontSize = '0.8vw';
        });

        document.querySelectorAll('.card:nth-child(2) .mid > div').forEach(item => {
            item.classList.add('edit-mode');
            item.addEventListener('click', handleEditClick);
        });

        button.innerHTML = 'Cancel';
        isEditMode = true;
    } else {
        document.querySelectorAll('.card:nth-child(2) .mid .subtitle').forEach(item => {
            item.style.fontSize = '1.3vw';
        });

        document.querySelectorAll('.card:nth-child(2) .mid > div').forEach(item => {
            item.classList.remove('edit-mode');
            item.removeEventListener('click', handleEditClick);
        });

        button.innerHTML = '<i class="fas fa-pencil-alt"></i> Edit';
        isEditMode = false;
    }
});
});

// Para o card 3
document.querySelectorAll('.card:nth-child(3) .edit_btn').forEach(button => {
let isEditMode = false;

button.addEventListener('click', () => {
    if (!isEditMode) {
        document.querySelectorAll('.card:nth-child(3) .mid .subtitle').forEach(item => {
            item.style.setProperty('font-size', '0.8vw', 'important');
        });

        document.querySelectorAll('.card:nth-child(3) .mid > div').forEach(item => {
            item.classList.add('edit-mode');
            item.addEventListener('click', handleEditClick);
        });

        button.innerHTML = 'Cancel';
        isEditMode = true;
    } else {
        document.querySelectorAll('.card:nth-child(3) .mid .subtitle').forEach(item => {
            item.style.fontSize = '1.3vw';
        });

        document.querySelectorAll('.card:nth-child(3) .mid > div').forEach(item => {
            item.classList.remove('edit-mode');
            item.removeEventListener('click', handleEditClick);
        });

        button.innerHTML = '<i class="fas fa-pencil-alt"></i> Edit';
        isEditMode = false;
    }
});
});

//Redireciona os dados de edição para o link correspondente
function handleEditClick(event) {
let elementId = event.currentTarget.querySelector('span').id;

// Redireciona com base no dado clicado
if (elementId === 'first_name_display') {
    window.location.href = 'name';
} else if (elementId === 'email_display') {
    window.location.href = 'email';
} else if (elementId === 'phone_display') {
    window.location.href = 'phone';
} else if (elementId === 'password_display') {
    window.location.href = 'password';
} else if (elementId === 'language_display') { 
    window.location.href = '/language';
} else if (elementId === 'theme_display') {
    window.location.href = '/theme';
} else if (elementId === 'postal_code_display') {
    window.location.href = 'cep';
}
}

//Seleciona os botões de navegação internos, os que ficam dentro do account
const navButtons = document.querySelectorAll('.nav_btn');
const myProfileBtn = document.getElementById('my_profile');
let timeout;  //armazena o timeout

// Define 'My Profile' como selecionado inicialmente
myProfileBtn.classList.add('selected');

navButtons.forEach(button => {
    button.addEventListener('mouseover', () => {
        //tira a  seleçao do 'My Profile' qnd passar o mouse por cima de outro
        myProfileBtn.classList.remove('selected');
        if (timeout) {
            clearTimeout(timeout);  //Limpa o timeout se houver
        }
    });

    button.addEventListener('mouseout', () => {
        //Se nenhum botão estiver em hover, espera 0.5s antes de voltar a selecionar 'My Profile'
        timeout = setTimeout(() => {
            const isAnyButtonHovered = Array.from(navButtons).some(btn => btn.matches(':hover'));
            if (!isAnyButtonHovered) {
                myProfileBtn.classList.add('selected');
            }
        }, 30);  // tempo de atraso pro selected voltar pro 'My profile'
    });
});