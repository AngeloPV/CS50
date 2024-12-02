
const sideNavButtons = document.querySelectorAll('.side-nav_btn');
const historySideNavBtn = document.getElementById('history');  // Botão "History" da sidebar


let timeout; 
// Funcao responsavel por ajustar a seleção da side nav bar
historySideNavBtn.classList.add('selected');

sideNavButtons.forEach(button => {
    button.addEventListener('mouseover', () => {
        historySideNavBtn.classList.remove('selected');
        if (timeout) {
            clearTimeout(timeout);  
        }
    });

    button.addEventListener('mouseout', () => {
        timeout = setTimeout(() => {
            const isAnyButtonHovered = Array.from(sideNavButtons).some(btn => btn.matches(':hover'));
            if (!isAnyButtonHovered) {
                historySideNavBtn.classList.add('selected');
            }
        }, 30); 
    });
});

const mainNavButtons = document.querySelectorAll('.nav_btn');
const allMainNavBtn = document.getElementById('all');

// inicia marcando o botão "all" como selecionado
allMainNavBtn.classList.add('selected');

// Função para ajustar as seleções da main nav bar
mainNavButtons.forEach(button => {
    button.addEventListener('mouseover', () => {
        if (timeout) {
            clearTimeout(timeout);
        }
    });

    button.addEventListener('mouseout', () => {
        timeout = setTimeout(() => {
            const isAnyButtonHovered = Array.from(mainNavButtons).some(btn => btn.matches(':hover'));
            if (!isAnyButtonHovered && !document.querySelector('.nav_btn.selected')) {
                allMainNavBtn.classList.add('selected');
            }
        }, 30);
    });

    button.addEventListener('click', () => {
        // Remove a classe selected de todos os botões qnd clicar em um botão especifico
        mainNavButtons.forEach(btn => btn.classList.remove('selected'));
        allMainNavBtn.classList.remove('selected'); // Garante que "all" não fique selecionado

        // Adiciona a classe selected ao botão clicado
        button.classList.add('selected');
    });
});

// Evento específico para o botão all para restaurar a seleção
allMainNavBtn.addEventListener('click', () => {
    // Remove a classe selected de todos os botões
    mainNavButtons.forEach(btn => btn.classList.remove('selected'));

    // Adiciona a classe selected ao botão all de novo
    allMainNavBtn.classList.add('selected');
});



//Funcao responsavel por filtrar os itens do historico
document.addEventListener("DOMContentLoaded", () => {
    const navButtons = document.querySelectorAll(".nav_btn");
    const historyItems = document.querySelectorAll(".history-iten");

    navButtons.forEach(button => {
        button.addEventListener("click", () => {
            const filterType = button.id; // Pega o ID referente ao botão (all, buy, sell ou trade)

            historyItems.forEach(item => {
                if (filterType === "all") {
                    // Se estiver no all mostra todos os itens
                    item.style.display = "flex";
                } else {
                    // Se estiverem qlqr outro, vai mostrar so o item correspondente ao tipo
                    const itemType = item.querySelector(".content-title").textContent.toLowerCase();
                    item.style.display = itemType === filterType ? "flex" : "none";
                }
            });
        });
    });
});



function openModal(id, type) {
    // Filtrar o item correto de historyData com base no ID e no tipo
    const row = historyData.find(item => item.id == id && item.type == type);

    if (!row) {
        alert('Dados não encontrados!');
        return;
    }
    
    // Preencher os campos do modal com base no item selecionado
    document.getElementById('modal-id').textContent = row.id;
    document.getElementById('modal-date').textContent = row.date;
    document.getElementById('modal-type').textContent = row.type;
    document.getElementById('modal-amount').textContent = row.amount || row.amount_sender;
    document.getElementById('modal-value').textContent = 
    '$' + ((row.cost || row.value || row.rate)?.toFixed(2) || '0.00');

    // Verificação para mostrar "Moeda Enviada" e "Moeda Recebida" ou apenas "Moeda"
    if (row.cripto_sender_id && row.cripto_recipient_id) {
        // Exibe "Moeda Enviada" e "Moeda Recebida"
        document.getElementById('modal-currency-sender').textContent = row.cripto_sender_id === 1 
            ? 'Bitcoin (BTC)' 
            : row.cripto_sender_id === 2 
            ? 'Ethereum (ETH)' 
            : 'Desconhecida';
        document.getElementById('modal-amount-sender').textContent = row.amount_sender;

        document.getElementById('modal-currency-recipient').textContent = row.cripto_recipient_id === 1 
            ? 'Bitcoin (BTC)' 
            : row.cripto_recipient_id === 2 
            ? 'Ethereum (ETH)' 
            : 'Desconhecida';
        document.getElementById('modal-amount-recipient').textContent = row.amount_recipient;

        // Mostra os campos de moeda enviada e recebida
        document.getElementById('currency-sender-container').style.display = 'block';
        document.getElementById('currency-recipient-container').style.display = 'block';
        document.getElementById('currency-container').style.display = 'none';

        //Centraliza o modal

        document.getElementById('historyModal').style.top = "-40px";
        document.getElementById('historyModal').style.height = "150%";

    } else {
        // Exibe apenas "Moeda"
        const currency = row.criptocurrencies_id === 1 
            ? 'Bitcoin (BTC)' 
            : row.criptocurrencies_id === 2 
            ? 'Ethereum (ETH)' 
            : 'Desconhecida';
        
        document.getElementById('modal-currency').textContent = currency;

        // Mostra o campo de moeda e oculta os outros
        document.getElementById('currency-container').style.display = 'block';
        document.getElementById('currency-sender-container').style.display = 'none';
        document.getElementById('currency-recipient-container').style.display = 'none';

        //Centraliza o modal
        document.getElementById('historyModal').style.top = "0";
        document.getElementById('historyModal').style.height = "100%";
    }

    // Exibir o modal
    document.getElementById('historyModal').style.display = "block";
}

function closeModal() {
    const hasMsg = document.getElementById('config').dataset.hasMsg === 'true'

    // Ocultar o modal
    document.getElementById('historyModal').style.display = "none";
    if (hasMsg){
        window.location.href = "/manage/index";
    }
}

window.onclick = function (event) {
    const hasMsg = document.getElementById('config').dataset.hasMsg === 'true'
    
    var modal = document.getElementById('historyModal');
    var sellModal = document.getElementById('sellModal');
    if (event.target === modal) {
        document.getElementById('historyModal').style.display = "none";
        if (hasMsg){
            window.location.href = "/manage/index";
        }

    } else if (event.target === sellModal) {
        document.getElementById('sellModal').style.display = "none";
        if (hasMsg){
            window.location.href = "/manage/index";
        }

    }

};


function openSellModal(currency) {
    document.getElementById('sell-modal-title').textContent = currency
    
    //pega os valores salvos na data na declaração da div sellModal
    const modalElement = document.getElementById('sellModal');
    const sellCurrencyInput = document.getElementById('sell-currency');


    const bitcoin_balance = modalElement.dataset.bitcoinBalance;
    const ethereum_balance = modalElement.dataset.ethereumBalance;
    const bitcoin_price = modalElement.dataset.bitcoinPrice;
    const ethereum_price = modalElement.dataset.ethereumPrice;

    // Pega o campo pra definir o limite
    const sellAmountInput = document.getElementById('sell-amount');

    if (currency === 'bitcoin') {
        document.getElementById('sell-modal-total').textContent =  bitcoin_balance ;
        sellAmountInput.max = bitcoin_balance; 
        document.getElementById('sell-modal-value').textContent = 
        '$' + (bitcoin_price ? (bitcoin_balance * bitcoin_price).toFixed(2) : '0.00');    

    } else if (currency === 'ethereum') {
        document.getElementById('sell-modal-total').textContent =  ethereum_balance ;
        sellAmountInput.max = ethereum_balance; 
        document.getElementById('sell-modal-value').textContent = 
        '$' + (ethereum_price ? (ethereum_balance * ethereum_price).toFixed(2) : '0.00');
    }

    sellCurrencyInput.value = currency;
    document.getElementById('sellModal').style.display = "block";
}

function closeSellModal() {
    // Ocultar o modal
    const hasMsg = document.getElementById('config').dataset.hasMsg === 'true'

    document.getElementById('sellModal').style.display = "none";
    if (hasMsg){
        window.location.href = "/manage/index";
    }

}

// Evento para atualizar o valor aproximado conforme o usuário digita
document.getElementById('sell-amount').addEventListener('input', function () {
    const modalElement = document.getElementById('sellModal');
    const currency = document.getElementById('sell-modal-title').textContent.toLowerCase();

    const sellAmount = parseFloat(this.value) || 0; // Quantidade digitada pelo usuário

    let balance = 0;
    let price = 0;

    // Pega o saldo e o preço com base na moeda selecionada
    if (currency === 'bitcoin') {
        balance = parseFloat(modalElement.dataset.bitcoinBalance);
        price = parseFloat(modalElement.dataset.bitcoinPrice);
    } else if (currency === 'ethereum') {
        balance = parseFloat(modalElement.dataset.ethereumBalance);
        price = parseFloat(modalElement.dataset.ethereumPrice);
    }

    // Calcula o valor aproximado
    const sellValue = (sellAmount * price).toFixed(2);
    document.getElementById('sell-modal-value-form').textContent = `$${sellValue}`;
});