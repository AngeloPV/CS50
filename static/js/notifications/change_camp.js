var socket = io.connect('/notifications');

socket.on('connect', function() {
    console.log('Connected to /notifications namespace');
});

function show_notificaitons(type) {
    socket.off('change_type');

    socket.emit('change_type', type)

    var hidden = document.getElementById('myHiddenInput');
    hidden.value = type;

    socket.on('change_type', (data) => {
        // Um pequeno atraso pode ajudar
        teste(data, type)
    })
}

function teste(data, type) {
    const receivedData = JSON.parse(data.data); // Converter a string JSON de volta para um objeto
    
    var hidden = document.getElementById('myHiddenInput');
    hidden.value = type
    console.log("Tipo de notificação:", hidden.value);  // Logar o tipo para depuração

    var tbody = document.getElementById('data-table-body');


       // Verificar se não há notificações
    if (receivedData == null || receivedData.length === 0) {
        console.log("Nenhuma notificação disponível.");
        tbody.innerHTML = '';
        reassignEventListeners();  // Reatribuir eventos após a mudança

        return;
    }

    tbody.innerHTML = '';

    receivedData.forEach(row => {
        if (row[5] == 0) {
            var newRow = `<tr>
                <td class="line_checkbox">
                    <input type="checkbox" class='checkbox' value="${row[4]}">${ row[1] }
                    <i class="fas fa-file notifcationsProx" title="Desarquivar" style="overflow: hidden; width: 50%; display: inline-block;"></i>
                    <i class="fas fa-star favoriteProx" title="Favoritar"></i>
                    <i class="fas fa-archive archivrProx" title="Arquivar"></i>
                    <i class="fas fa-envelope-open-text readProx" title="Ler"></i>
                    <i class="fas fa-trash deleteButtons" title="Deletar"></i>
                </td>
            </tr>`;
            tbody.innerHTML += newRow;  // Adiciona uma nova linha
        } else {
            var newRow = `<tr>
                <td class="line_checkbox">
                    <input type="checkbox" class='checkbox' value="${row[4]}"><b>${row[1]}</b>
                    <i class="fas fa-bell notifcationsProx" title="Notificações"></i>
                    <i class="fas fa-star favoriteProx" title="Favoritar"></i>
                    <i class="fas fa-archive archivrProx" title="Arquivar"></i>
                    <i class="fas fa-envelope-open-text readProx" title="Ler"></i>
                    <i class="fas fa-trash deleteButtons" title="Deletar"></i>
                </td>
            </tr>`;
            tbody.innerHTML += newRow;  // Adiciona uma nova linha
        }
    })

    reassignEventListeners();  // Reatribuir eventos após a mudança
}
