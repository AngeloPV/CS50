
// Obtém o modal e o botão de fechar
const modal = document.getElementById("myModal");
const span = document.querySelector(".close");
const cryptoNameElement = document.getElementById("cryptoName");

// Função para abrir o modal com o nome da moeda
function openModal(cryptoName) {
    cryptoNameElement.textContent = cryptoName; // Define o nome da moeda no modal
    modal.style.display = "block"; // Mostra o modal
}

// Fecha o modal ao clicar no "x"
span.onclick = function () {
    modal.style.display = "none";
};

// Fecha o modal ao clicar fora dele
window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};
