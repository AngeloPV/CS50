function your_trades() {
    var your_trades = document.getElementById('your_trades');
    
    your_trades.addEventListener('click', () => {
        if (cond_change == 'all_trade' && your_trades.value == 'all_trade') {
            cond_change = 'your_trade';
        } else if (cond_change == 'your_trade' && your_trades.value == 'your_trade'){
            cond_change = 'all_trade';
        }

        if (your_trades.value == 'your_trade') {
            your_trades.value = 'all_trade'
        } else {
            your_trades.value = 'your_trade'
        }

        send_change(your_trades)
    })
}

function send_change(your_trades) {
    if (your_trades.value == 'your_trade') {
        socket.emit('your_trade', true)
        type = 'your_trade'

        socket.on('your_trade', (data) => {
            change_html(data, type)
        })

        your_trades.textContent = "";
        your_trades.innerHTML += "<i class='fa-solid fa-backward'></i> Return";
    } else {
        socket.emit('your_trade', false)
        type = 'all_trade'

        socket.on('your_trade', (data) => {
            change_html(data, type)
        })

        your_trades.textContent = "";
        your_trades.innerHTML += "<i class='fa-solid fa-eye'></i> Your Trades";
    }
}
