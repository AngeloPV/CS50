function selected_actions(hidden) {
    var archive_selected = document.getElementById('archive_selected');
    archive_selected.replaceWith(archive_selected.cloneNode(true));  // Remove listeners antigos

    var archive_selected = document.getElementById('archive_selected');  // Redefine variável
    archive_selected.addEventListener('click', () => {
        change_type_all('archive', hidden.value, getVisibleCheckboxes())
    });

    var favorite_selected = document.getElementById('favorite_selected');
    favorite_selected.replaceWith(favorite_selected.cloneNode(true));  // Remove listeners antigos

    var favorite_selected = document.getElementById('favorite_selected');  // Redefine variável
    favorite_selected.addEventListener('click', () => {
        change_type_all('favorite', hidden.value, getVisibleCheckboxes())
    });


    var standard_selected = document.getElementById('standard_selected');
    standard_selected.replaceWith(standard_selected.cloneNode(true));  // Remove listeners antigos

    var standard_selected = document.getElementById('standard_selected');  // Redefine variável
    standard_selected.addEventListener('click', () => {
        change_type_all('standard', hidden.value, getVisibleCheckboxes())
    });

    var read_selected = document.getElementById('read_selected');
    read_selected.replaceWith(read_selected.cloneNode(true));  // Remove listeners antigos

    var read_selected = document.getElementById('read_selected');  // Redefine variável
    read_selected.addEventListener('click', () => {
        change_type_all(0, hidden.value, getVisibleCheckboxes())
    });
}
