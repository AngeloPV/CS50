var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];

// Exibe o modal
window.onload = function() {
    modal.style.display = "block";
}


// Fecha o modal no x
span.onclick = function() {
    modal.style.display = "none";
}

// Fecha ao clicar flora
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
