
function change_type_all(value_update, actual_type, checkboxes_send) {
    socket.off('change_type');

    checkboxes_verify = Array.from(checkboxes_send); // nodelist to array

    const allAreCheckboxes = checkboxes_verify.every(item => // allAreCheckboxes is true or false
        item instanceof HTMLInputElement && item.type === 'checkbox' // verify if the checkboxes_send has a input_checkbox
    )
    console.log(allAreCheckboxes);  // Retorna true se todos forem checkboxes, caso contrário false.

    
    if (Number.isInteger(parseInt(checkboxes_send))) {
        var checkboxes = parseInt(checkboxes_send)
        console.log(checkboxes)

        socket.emit('verify_type', value_update, checkboxes, actual_type);

        socket.on('verify_type', (data) => {
            change_html(data, actual_type)
        });
    } else if (allAreCheckboxes) {
        var checkboxes = selectCheckbox(checkboxes_send)

        // Emitir um evento para o servidor
        socket.emit('verify_type', value_update, checkboxes, actual_type);

        socket.on('verify_type', (data) => {
            change_html(data, actual_type)
        });
    }
}
