function show_notificaitons(type) {
    socket.off('change_type');

    socket.emit('change_type', type)

    var hidden = document.getElementById('myHiddenInput');
    hidden.value = type;

    socket.on('change_type', (data) => {
        // Um pequeno atraso pode ajudar
        change_html(data, type);  // Verifique se o valor está correto aqui
    })
}


function change_html(data, type) {
    const receivedData = JSON.parse(data.data); //Convert a JSON string back to an object

    var receiveCount = JSON.parse(data.count)

    let count_past = document.querySelectorAll('.radient')
    let count_all = document.getElementById('count_all')

    count_past.forEach((count_p) => {
        count_p.innerHTML = ''

        for (let type_count in receiveCount) {
            if (receiveCount.hasOwnProperty(type_count)) {
                count_p.innerHTML = receiveCount[type_count] 

                delete receiveCount[type_count]
                
                break;
            }
        }
    })

    count_all.innerHTML = receiveCount['all'] + ' Notifications'

    // each time change the types of notifications, the actionsSelected opacity needs change to zero
    var actionsSelect = document.querySelector('.actionsSelected')
    actionsSelect.style.opacity = 0

    var hidden = document.getElementById('myHiddenInput');
    hidden.value = type
    

    // update icons according to notification type
    var actionsSelected = document.querySelector('.actionsSelected')
    var button_standard = document.getElementById('moveNotification')
    var selectedCheckbox = document.getElementById('selectedCheckbox')

    if (hidden.value == 'archive') {
        selectedCheckbox.checked = false

        button_standard.style.display = 'block'
        button_standard.innerHTML = 'Unarchive All'

        actionsSelected.innerHTML = `<i class="fas fa-star" id="favorite_selected" title="Favorite Selected"></i>
        <i class="fa-regular fa-folder-open standard_selected" title="Unarchive Selected"></i>
        <i class="fas fa-envelope-open-text" id="read_selected" title="Read Selected"></i>
        <i class="fas fa-trash" id="delete_selected" title="Deletar"></i>`
    } else if (hidden.value == 'favorite') {
        selectedCheckbox.checked = false

        button_standard.style.display = 'block'
        button_standard.innerHTML = 'Unfavorite All'

        actionsSelected.innerHTML = `<i class='fa-regular fa-star standard_selected ' title="Unfavorite Selected"></i>
        <i class="fas fa-archive" id="archive_selected" title="Archive Selected"></i>
        <i class="fas fa-envelope-open-text" id="read_selected" title="Read Selected"></i>
        <i class="fas fa-trash" id="delete_selected" title="Deletar"></i>`
    }else {
        selectedCheckbox.checked = false

        button_standard.style.display = 'none'

        actionsSelected.innerHTML = `<i class="fas fa-star" id="favorite_selected" title="Favorite Selected"></i>
        <i class="fas fa-archive" id="archive_selected" title="Archive Selected"></i>
        <i class="fas fa-envelope-open-text" id="read_selected" title="Read Selected"></i>
        <i class="fas fa-trash" id="delete_selected" title="Deletar"></i>`
    }
    

    var div_notifications = document.querySelector('.notifications')


    // Verificar se não há notificações
    if (!Array.isArray(receivedData) || receivedData == null || receivedData.length === 0) {
        console.log("Nenhuma notificação disponível.");
        
        div_notifications.innerHTML = ''
        
        reassignEventListeners();  // Reatribuir eventos após a mudança

        return;
    }

    div_notifications.innerHTML = ''

    receivedData.forEach(row => {
        var new_icons
        if (hidden.value == 'archive') { 
            new_icons = `<div class="actions">
            <i class="fas fa-star favoriteProx" title="Favorite"></i>
            <i class="fa-regular fa-folder-open notifcationsCSS notifcationsProx" title="Unarchive"></i>
            <i class="fas fa-envelope-open-text readProx" title="Ler"></i>
            <i class="fas fa-trash deleteButtons" title="Delete"></i>
            </div>`
        } else if (hidden.value == 'favorite') {
            new_icons = `<div class="actions">
            <i class='fa-regular fa-star notifcationsCSS notifcationsProx' title="Unfavorite"></i>
            <i class="fas fa-archive archiveProx" title="Archive"></i>
            <i class="fas fa-envelope-open-text readProx" title="Read"></i>
            <i class="fas fa-trash deleteButtons" title="Delete"></i>
            </div>`
        } else {
            new_icons = `<div class="actions">
            <i class="fas fa-star favoriteProx" title="Favorite"></i>
            <i class="fas fa-archive archiveProx" title="Archive"></i>
            <i class="fas fa-envelope-open-text readProx" title="Ler"></i>
            <i class="fas fa-trash deleteButtons" title="Delete"></i>
            </div>`
        }
        

        let newRow;
        if (row[5] == 0) {
            newRow = `<section class="notification-item" style="background-color: #f8f9fae9;">
                    <input type="checkbox" class='checkbox' value="${row[4]}">
                    <div class="content">${row[1]}</div>
                    <div class="time">${row[6]}</div>
                        ${new_icons}
                </section>`
        } else {
            newRow = `<section class="notification-item" style="background-color: #f8f9fae9;">
                <input type="checkbox" class='checkbox' value="${row[4]}">
                <div class="content"><b>${row[1]}</b></div>
                <div class="time">${row[6]}</div>
                <div class="actions">
                    ${new_icons}
                </div>
            </section>`
        }
    
        div_notifications.innerHTML += newRow
    })

    reassignEventListeners();  // Reatribuir eventos após a mudança
}
