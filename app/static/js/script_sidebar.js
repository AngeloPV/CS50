//ALTERA OS SUB MENUS
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const submenus = document.querySelectorAll('.submenu');

    sidebar.addEventListener('mouseleave', () => {
        // Fecha todos os submenus quando a sidebar é recolhida
        submenus.forEach(submenu => {
            submenu.style.display = 'none';
        });
    });

    // Adicione um listener para o clique fora da sidebar para fechar o submenu
    document.addEventListener('click', (event) => {
        if (!sidebar.contains(event.target)) {
            submenus.forEach(submenu => {
                submenu.style.display = 'none';
            });
        }
    });

    // Adiciona um listener para abrir o submenu correspondente ao clicar em um item de menu
    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(item => {
        item.addEventListener('click', (event) => {
            event.stopPropagation(); // Impede que o clique se propague para o document
            const submenu = item.nextElementSibling; // Seleciona o submenu imediatamente após o item de menu
            if (submenu && submenu.classList.contains('submenu')) {
                // Alterna a visibilidade do submenu
                if (submenu.style.display === 'block') {
                    submenu.style.display = 'none';
                } else {
                    // Fecha todos os outros submenus
                    submenus.forEach(sub => {
                        if (sub !== submenu) {
                            sub.style.display = 'none';
                        }
                    });
                    submenu.style.display = 'block';
                }
            }
        });
    });
});

//REDIRECIONA OS ITENS DA SIDEBAR
document.addEventListener('DOMContentLoaded', () => {
    // Define os caminhos para redirecionamento
    const paths = {
        'comprar': '/caminho/para/pagina/comprar',
        'vender': '/caminho/para/pagina/vender',
        'gerenciar': '/caminho/para/pagina/gerenciar',
        'meus-depositos': '/caminho/para/pagina/gerenciar',
        'depositar-opcao': '/caminho/para/pagina/gerenciar',
        'alterar-dados': '/caminho/para/pagina/gerenciar',
        'temas-e-idioma': '/caminho/para/pagina/temas-e-idioma',
        'logout': '/caminho/para/pagina/logout',
        'notificacao': '/caminho/para/pagina/notificacao',
        'perfil_foto': '/caminho/para/pagina/perfil',
    };

    // Adiciona event listeners para os itens de menu
    Object.keys(paths).forEach(itemId => {
        const menuItem = document.getElementById(itemId);
        if (menuItem) {
            menuItem.addEventListener('click', () => {
                window.location.href = paths[itemId];
            });
        }
    });
});

//Exibe a sidebar em dispositivos moveis
document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            // Remove classes de animação anteriores, se houver
            sidebar.classList.remove('expand-animation', 'contract-animation');

            // Adiciona a classe de animação apropriada
            if (sidebar.classList.contains('expanded')) {
                sidebar.classList.add('contract-animation');
                sidebar.classList.remove('expanded');
            } else {
                sidebar.classList.add('expand-animation');
                sidebar.classList.add('expanded');
            }

            // Após a animação, removemos a classe para permitir que a animação possa ser reaplicada no próximo clique
            setTimeout(() => {
                sidebar.classList.remove('expand-animation', 'contract-animation');
            }, 300); // Tempo de animação em milissegundos
        });
    } else {
        console.error('Elementos não encontrados no DOM.');
    }
});
