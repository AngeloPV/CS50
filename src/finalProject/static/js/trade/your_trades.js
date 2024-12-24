function your_trades() {
    var your_trades = document.getElementById('your_trades');
    
    var type = null

    your_trades.addEventListener('click', () => {
        console.log(your_trades.value)
        if (your_trades.value == 'your_trade') {
            your_trades.value ='all_trade'
        } else {
            your_trades.value = 'your_trade'
        }
        send_change(your_trades)
    })
}
// fazer uma variavel global com que guarde a pagina anterior, assim verificando e puxando o conteudo

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

