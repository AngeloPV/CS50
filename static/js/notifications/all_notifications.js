function all_notifcations(hidden) {
    var selectAll = document.getElementById('selectAll');
    selectAll.replaceWith(selectAll.cloneNode(true));  // Remove os listeners antigos O importante é que os event listeners não são copiados para o novo nó, por isso usamos esse método para "limpar" os listeners existentes

    selectAll = document.getElementById('selectAll');  // Redefine a variável
    selectAll.addEventListener('click', () => {
        let checkboxes = getVisibleCheckboxes(); 
        allCheckbox(checkboxes)
        checkboxes.forEach(function (checkbox) {
            // console.log(checkbox);
        });
    });


    // Listener para o botão de arquivar todos
    var archiveAll = document.getElementById('archiveAll');
    archiveAll.replaceWith(archiveAll.cloneNode(true));  // Remove listeners antigos

    archiveAll = document.getElementById('archiveAll');  // Redefine variável
    archiveAll.addEventListener('click', () => {
        allCheckbox(getVisibleCheckboxes(), hidden.value, 'archive');
    });


    // Listener para o botão de favoritar todos
    var favoriteAll = document.getElementById('favoriteAll');
    favoriteAll.replaceWith(favoriteAll.cloneNode(true));  // Remove listeners antigos

    favoriteAll = document.getElementById('favoriteAll');  // Redefine variável
    favoriteAll.addEventListener('click', () => {
        allCheckbox(getVisibleCheckboxes(), hidden.value, 'favorite');
    });


    // Listener para o botão de mover notificações
    var moveNotificationall = document.getElementById('moveNotification');
    moveNotificationall.replaceWith(moveNotificationall.cloneNode(true));  // Remove listeners antigos

    moveNotificationall = document.getElementById('moveNotification');  // Redefine variável
    moveNotificationall.addEventListener('click', () => {
        allCheckbox(getVisibleCheckboxes(), hidden.value, 'standard');
    });


    var readAll = document.getElementById('readAll');
    readAll.replaceWith(readAll.cloneNode(true));  // Remove listeners antigos


    readAll = document.getElementById('readAll');  // Redefine variável
    readAll.addEventListener('click', () => {
        allCheckbox(getVisibleCheckboxes(), hidden.value, 0);
    });

    var deleteAll = document.getElementById('deleteAll');
    deleteAll.replaceWith(deleteAll.cloneNode(true));  // Remove listeners antigos


    deleteAll = document.getElementById('deleteAll');  // Redefine variável
    deleteAll.addEventListener('click', () => {
        allCheckbox(getVisibleCheckboxes(), hidden.value)
        let selectAll = selectCheckbox(getVisibleCheckboxes())
        delete_notifications(selectAll, hidden.value)
    });
}
