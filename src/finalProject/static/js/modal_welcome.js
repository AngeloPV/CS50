var modal = document.getElementById("carouselModal");
var slides = document.getElementsByClassName("carousel-slide");
var currentSlide = 0;

//exibe o modal
window.onload = function() {
    modal.style.display = "block";
    
    const stats = "{{ stats|escapejs }}"; 
    console.log("Status do Modal:", stats); 

    let slideIndex = 0;
    if (stats = 'denied') {
        slideIndex = 2; 
    } else {
        slideIndex = 0; 
    }

    showSlide(slideIndex);
};

// Função para trocar de slide
function changeSlide(n) {
    currentSlide += n;
    if (currentSlide >= slides.length) {
        currentSlide = slides.length - 1; 
    } else if (currentSlide < 0) {
        currentSlide = 0;
    }
    showSlide(currentSlide);
}

// Função para exibir o slide atual
function showSlide(n) {
    // Oculta todos os slides
    for (var i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    // Exibe o slide atual
    slides[n].style.display = "flex";

}

// Função para mover o cursor para o próximo campo de entrada da senha
function moveToNext(current, nextFieldID) {
    if (current.value.length === 1 && nextFieldID) {
        document.getElementById(nextFieldID).focus();
    }
}


const closeButton = document.querySelector(".close");

// Fechar o modal ao clicar no botão de fechar
closeButton.onclick = function() {
    modal.style.display = "none";
}

// Fechar o modal ao clicar fora do conteúdo do modal
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}