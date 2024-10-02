
document.addEventListener('DOMContentLoaded', () => {
    reassignEventListeners();

    // Listeners para os botões de troca de tipo de notificações
    var archive_change = document.getElementById('changeArchive');
    archive_change.addEventListener('click', () => {
        show_notificaitons('archive');
    });

    // Listeners para os botões de troca de tipo de notificações
    var standard_change = document.getElementById('standardArchive');
    standard_change.addEventListener('click', () => {
        show_notificaitons('standard');
    });

    var favorite_change = document.getElementById('changeFavorite');
    favorite_change.addEventListener('click', () => {
        show_notificaitons('favorite');
    });
});

function getVisibleCheckboxes() {
    var checkboxes = document.querySelectorAll('.checkbox');
    return Array.from(checkboxes).filter(function(checkbox) {
        return checkbox.offsetParent !== null;  // Verifica se o elemento está visível (presente no DOM)
    });
}

// Função para reatribuir listeners após cada atualização de notificações
function reassignEventListeners() {
    // var checkboxes = document.querySelectorAll('.checkbox')

    var hidden = document.getElementById('myHiddenInput');
    // console.log(hidden);


    var line_checkbox = document.querySelectorAll('.line_checkbox');
    line_checkbox.forEach(button => {
        button.replaceWith(button.cloneNode(true));  // Remove listeners antigos
    });
    
    line_checkbox = document.querySelectorAll('.line_checkbox');  // Redefine variável
    line_checkbox.forEach(button => {
        button.addEventListener('click', () => {
            var closest_checkbox = button.closest('tr').querySelector('.checkbox')
            closest_checkbox.checked = true
            console.log(closest_checkbox)
        });
    });

    all_notifcations(hidden)
    prox_notifications(hidden)
    selected_actions(hidden)


    // Listener para o botão de deletar notificações
    var button_delete = document.getElementById('deleteButton');
    button_delete.replaceWith(button_delete.cloneNode(true));  // Remove listeners antigos

    button_delete = document.getElementById('deleteButton');  // Redefine a variável
    button_delete.addEventListener('click', function (event) {
        var restult_checkboxes = selectCheckbox(getVisibleCheckboxes());
        delete_notifications(restult_checkboxes, hidden.value);
    });
}
