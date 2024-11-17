function delete_notifications(checkboxes, actual_type) {
    var checkboxe_values = checkboxes
    console.log(checkboxe_values)

    if (checkboxe_values.length > 0 && Array.isArray(checkboxe_values)) {
        send_back(checkboxe_values, actual_type)
    } else if (Number.isInteger(parseInt(checkboxe_values))) {
        // console.log(actual_type)
        send_back(parseInt(checkboxe_values), actual_type)
    }    
}



function send_back(restult_checkboxes, actual_type) {
    socket.off('delete');

    socket.emit('delete', restult_checkboxes, actual_type);

    socket.on('delete', (data) => {
        change_html(data, actual_type)
    }); 
}
