if (window.history.replaceState) {
    // Substitui o estado atual do histórico para evitar o reenvio de formulários ao recarregar a página
    window.history.replaceState(null, null, window.location.href);
}

//Aplica uma mascara no cpf pra ficar no formato 000.000.000-00
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

// Aplica uma mascara no telefone pra ficar no formato (00) 00000-0000
function Phonemask(phone) {
    let valor = phone.value.replace(/\D/g, '');
    
    if (valor.length <= 11) {
        valor = valor.replace(/(\d{2})(\d)/, '($1)$2')
        valor = valor.replace(/(\d{5})(\d)/, '$1-$2')
    }

    phone.value = valor;
}

