function delete_trades() {

    var div_deletes = document.querySelector('.btn_deletes')

    var btn_delete = document.getElementById('delete_trades')
    var your_trades = document.getElementById('your_trades');

    var delete_all = document.getElementById('delete_all')
    var select_none = document.getElementById('select_none')
    var delected_select = document.getElementById('delected_select')

    btn_delete.addEventListener('click', () => {
        div_deletes.style.display = 'flex'

        your_trades.textContent = "";
        your_trades.innerHTML += "<i class='fa-solid fa-eye'></i> All Trades";

        socket.emit('your_trade', true)
    
        type = 'checkbox'
    })

    socket.on('your_trade', (data) => {
        change_html(data, type)
    })


    delete_all.addEventListener('click', event => {
        const checkboxes = document.querySelectorAll('.checkbox');
    
        // Alterna o estado de todos os checkboxes
        checkboxes.forEach(checkbox => {
            checkbox.checked = true;
        });
        var text = 'All your trades will be deleted'
        send_data_delete(text, checkboxes)
    })

    delected_select.addEventListener('click', () => {
        const checkboxes = document.querySelectorAll('.checkbox');

        text = 'All selected trades will be deleted'
        send_data_delete(text, checkboxes)

    })

    socket.on('delete_trade', (data) => {
        socket.emit('your_trade', true)
        type = 'checkbox'
        
        socket.on('your_trade', (data) => {
            change_html(data, type)
        })    
    })

    select_none.addEventListener('click', event => {
        const checkboxes = document.querySelectorAll('.checkbox');
    
        // Alterna o estado de todos os checkboxes
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
    })


}


function send_data_delete(text, checkboxes) {
    var verify = false
    var selected = [];

    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            selected.push(checkbox.value);
            verify = true
        }
    });
    
    if (verify) {
        showCustomAlert(
            null,
            'Are you sure you want to delete?',
            `<p>${text}</p>`,
            'question',
            'Delete All',
            ["custom-title_sucess", "custom-succes-button"]
        );
    
        var btn_swal = document.querySelector('.custom-succes-button')
    
        if (btn_swal) {
            btn_swal.addEventListener('click', () => {
                socket.emit('delete_trade', selected)
            });
        } 
    } else {
        showCustomAlert(
            null,
            'You need to select at least one trade',
            null,
            'question',
            'Understood',
            ["custom-title_sucess", "custom-succes-button"]
        );
    }
}

function hideDeleteSection() {
    var div_deletes = document.querySelector('.btn_deletes')

    div_deletes.style.display = 'none';
}
