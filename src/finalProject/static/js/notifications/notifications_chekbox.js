var socket = io.connect('/notifications', {
    transports: ['websocket']
});

socket.on('connect', function() {
    console.log('Connected to /notifications namespace');
});

socket.on('disconnect', () => {
    console.log("WebSocket disconnected");
    checkSocketConnection(); // Tente reconectar quando desconectar
});

function checkSocketConnection() {
    if (!socket.connected) {
        socket.connect(); // Reconnect if disconnected
        console.log("Reconnected to WebSocket");
    }
}

window.addEventListener('beforeunload', () => {
    if (socket) {
        socket.disconnect();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    reassignEventListeners()
    checkSocketConnection()

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


function action_opacity() {
    var actionsSelect = document.querySelector('.actionsSelected')

    if (selectCheckbox(getVisibleCheckboxes()) == 'Error') {
        actionsSelect.style.opacity = 0
    } else {
        actionsSelect.style.opacity = 1
    }
}


// Função para reatribuir listeners após cada atualização de notificações
function reassignEventListeners() {
    // Add the class active in the type of notifications
    var span_types = document.querySelectorAll('.type')

    span_types.forEach(function(span) {
        span.addEventListener('click', function(e) {

            span_types.forEach(function(span_remove) {
                span_remove.classList.remove("active");
                span_remove.querySelector(".radient").classList.remove('active')
            });

            span.querySelector('.radient').classList.add("active");
            span.classList.toggle("active");
        })
    })
    

    var hidden = document.getElementById('myHiddenInput');

    all_notifcations(hidden)
    prox_notifications(hidden)
    selected_actions(hidden)

}
