// Mostra a lista de requisitos quando o campo de senha é clicado
document.getElementById('password').addEventListener('focus', function() {
    document.getElementById('password-requirements').style.display = 'block';
});

// Esconde a lista de requisitos quando o campo de senha perde o foco
document.getElementById('password').addEventListener('blur', function() {
    document.getElementById('password-requirements').style.display = 'none';
});

// Mostra a lista de requisitos quando o campo de confirmação de senha é clicado
document.getElementById('password-confirm').addEventListener('focus', function() {
    document.getElementById('password-requirements').style.display = 'block';
});

// Esconde a lista de requisitos quando o campo de confirmação de senha perde o foco
document.getElementById('password-confirm').addEventListener('blur', function() {
    document.getElementById('password-requirements').style.display = 'none';
});