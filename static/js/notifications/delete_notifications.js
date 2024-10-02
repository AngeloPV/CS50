function delete_notifications(checkboxes, actual_type) {
    var checkboxe_values = checkboxes
    // console.log(checkboxe_values)

    if (checkboxe_values.length > 0 && Array.isArray(checkboxe_values)) {
        send_back(checkboxe_values, actual_type)
    } else if (Number.isInteger(parseInt(checkboxe_values))) {
        // console.log(actual_type)
        send_back(parseInt(checkboxe_values), actual_type)
    }    
}

var socket = io.connect('/notifications');

function send_back(restult_checkboxes, actual_type) {
    socket.off('delete');
    console.log(actual_type)
    socket.emit('delete', restult_checkboxes, actual_type);

    socket.on('delete', (data) => {
        teste(data, actual_type)

        console.log('Received response: ' + data.data);
    }); 
}
