var socket = io.connect('/trade', {
    transports: ['websocket', 'polling']
});

var cond_change = 'all_trade'


function checkSocketConnection() {
    if (!socket.connected) {
        socket.connect(); // Reconnect if disconnected
        console.log("Reconnected to WebSocket");
    }
}

socket.on('disconnect', () => {
    console.log("WebSocket disconnected");
    checkSocketConnection(); // Tente reconectar quando desconectar
});

socket.on('connect', function() {
    console.log('Connected to /notifications namespace');
});

window.addEventListener('beforeunload', () => {
    if (socket) {
        socket.disconnect();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    checkSocketConnection();
    delete_trades()
    your_trades()
    add_trade()
    search_trades()
    open_modals()
})


function open_modals() {
    
    var open_modal = document.querySelectorAll(".open_modal")
    var close_modal = document.querySelectorAll(".close_modal")

    open_modal.forEach((button) => {
        button.addEventListener("click", () => {
            var id_modal = button.dataset.modal

            var types_modal = ['trade-details', 'y_trade-details']

            for (var i = 0; i < 2; i++) {
                if(types_modal[i] == id_modal) {
                    get_data_view(button.value, types_modal[i])
                    console.log(types_modal[i])
                    break

                }
            }

            var modal_open = document.getElementById(id_modal)

            if(modal_open) {
                modal_open.style.display = "flex"
            }
        })
    })

    close_modal.forEach((button) => {
        button.addEventListener("click", () => {
            var modal_close = button.closest(".modal")
            if(modal_close){
                modal_close.style.display = "none"
            }
        })
    })

    window.addEventListener("click", (event) => {
        var modals = document.querySelectorAll(".modal");
        modals.forEach((modal) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    });
}
