function selected_actions(hidden) {
    var archive_selected = document.getElementById('archive_selected');
    if (archive_selected !== null) {
        archive_selected.replaceWith(archive_selected.cloneNode(true));  // Remove listeners antigos

        var archive_selected = document.getElementById('archive_selected');  // Redefine variável
        archive_selected.addEventListener('click', () => {
            change_type_all('archive', hidden.value, getVisibleCheckboxes())
        });
    }

    var favorite_selected = document.getElementById('favorite_selected');
    if (favorite_selected !== null) {
        favorite_selected.replaceWith(favorite_selected.cloneNode(true));  // Remove listeners antigos

        var favorite_selected = document.getElementById('favorite_selected');  // Redefine variável
        favorite_selected.addEventListener('click', () => {
            change_type_all('favorite', hidden.value, getVisibleCheckboxes())
        });
    }

    var standard_selected = document.getElementById('standard_selected');
    if (standard_selected !== null) {
        standard_selected.replaceWith(standard_selected.cloneNode(true));  // Remove listeners antigos

        var standard_selected = document.getElementById('standard_selected');  // Redefine variável
        standard_selected.addEventListener('click', () => {
            change_type_all('standard', hidden.value, getVisibleCheckboxes())
        });
    }

    var read_selected = document.getElementById('read_selected');
    read_selected.replaceWith(read_selected.cloneNode(true));  // Remove listeners antigos

    var read_selected = document.getElementById('read_selected');  // Redefine variável
    read_selected.addEventListener('click', () => {
        change_type_all(0, hidden.value, getVisibleCheckboxes())
    });


    var delete_selected = document.getElementById('delete_selected');
    if (delete_selected !== null) {
        delete_selected.replaceWith(delete_selected.cloneNode(true));  // Remove listeners antigos

        var delete_selected = document.getElementById('delete_selected');  // Redefine variável
        delete_selected.addEventListener('click', () => {
            delete_notifications(selectCheckbox(getVisibleCheckboxes()), hidden.value)
        })
    }
}
