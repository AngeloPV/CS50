if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

function Cpfmask(cpf) {
    // Remove todos os caracteres que não são números
    let valor = cpf.value.replace(/\D/g, '');

    // Aplica a máscara
    if (valor.length <= 11) {
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2'); 
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2'); 
        valor = valor.replace(/(\d{3})(\d)/, '$1-$2'); 
    }

    // Atualiza o valor do input
    cpf.value = valor;
}

function Phonemask(phone) {
    let valor = phone.value.replace(/\D/g, '');
    
    if (valor.length <= 11) {
        valor = valor.replace(/(\d{2})(\d)/, '($1)$2')
        valor = valor.replace(/(\d{5})(\d)/, '$1-$2')
    }

    phone.value = valor;
}

