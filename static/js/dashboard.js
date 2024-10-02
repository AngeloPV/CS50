//Alterna entre os dados
function handleFlip(card) {
    card.classList.toggle('flipped');
    
    //Esconde a barra de rolagem e retorna depois de 2 segundos
    document.body.style.overflow = 'hidden'; 
    
    setTimeout(() => {
        document.body.style.overflow = ''; 
    }, 2000);

    // Captura todos os elementos dado1 e dado2
    const dados1 = document.querySelectorAll('.dado1');
    const dados2 = document.querySelectorAll('.dado2');

    // Alterna entre mostrar dado1 e dado2 para todos os cartões que tenham dado1 e dado2
    dados1.forEach((dado1, index) => {
        const dado2 = dados2[index];
        const isDado1Active = dado1.classList.contains('active');

        if (isDado1Active) {
            dado1.classList.add('exit');
            setTimeout(() => {
                dado1.classList.remove('active', 'exit'); // Remove o dado1
                dado1.style.display = 'none'; // Esconde o dado1
                dado2.classList.add('active'); // Adiciona o dado2
                dado2.style.display = 'flex'; // Mostra o dado2
            }, 600); // Tempo da animação
        } else {
            dado2.classList.add('exit');
            setTimeout(() => {
                dado2.classList.remove('active', 'exit'); // Remove o dado2
                dado2.style.display = 'none'; // Esconde o dado2
                dado1.classList.add('active'); //Adiciona o dado1
                dado1.style.display = 'flex'; //Mostra o dado1
            }, 600); // Tempo da animação
        }
    });
}

function initializeCardsVisibility() {
    // Captura todos os elementos dado1 e dado2
    const dados1 = document.querySelectorAll('.dado1');
    const dados2 = document.querySelectorAll('.dado2');

    dados1.forEach((dado1, index) => {
        const dado2 = dados2[index];
        // Verifica se dado1 está ativo e ajusta a visibilidade
        if (dado1.classList.contains('active')) {
            dado1.style.display = 'flex'; // Mostra dado1
            dado2.style.display = 'none'; // Esconde dado2
        } else {
            dado1.style.display = 'none'; // Esconde dado1
            dado2.style.display = 'flex'; // Mostra dado2
        }
    });
}

//Carrega o preloader quando a pagina for carregada
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    const content = document.querySelector('.content');

    // Inicializa a visibilidade dos cartões ao carregar a página
    initializeCardsVisibility();

    // Aguarda 1 segundo antes de remover o preloader
    setTimeout(() => {
        preloader.classList.add('hidden'); //Adiciona a classe para a transição de saída
        setTimeout(() => {
            preloader.style.display = 'none'; // Remove o preloader do fluxo do DOM
            content.classList.add('visible'); //Mostra o conteúdo da página
        }, 600); // Tempo da transição de saída 
    }, 0); // Tempo de exibição do preloader (tempo da animacao, apenas)
});

//Esconde a barra de rolagem nos primeiros 2 segundos de quando carrega a pagina
document.addEventListener('DOMContentLoaded', function() {
    document.body.style.overflow = 'hidden'; // Esconde a barra de rolagem
    
    // Aguarda 2 segundos e reativa a barra de rolagem
    setTimeout(() => {
        document.body.style.overflow = ''; //Restaura a barra de rolagem
    }, 2000);
});