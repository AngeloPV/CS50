function view_your_trade(data) {
    var dic_data = JSON.parse(data.response)
    var dic_address = JSON.parse(data.user_adress)
    var dic_trades = JSON.parse(data.trades)

    var your_address = document.getElementById('your_address')
    
    var Y_coin_sender = document.getElementById('Y_coin_sender')
    var Y_coin_receive = document.getElementById('Y_coin_receive')

    var Y_min_value = document.getElementById('Y_min_value')
    var Y_max_value = document.getElementById('Y_max_value')

    var Y_trade_amount = document.getElementById('Y_trade_amount')

    var Y_total_received = document.getElementById('Y_total_received')

    var Y_date = document.getElementById('Y_date')
    var Y_exchangers = document.getElementById('Y_exchangers')

    if (dic_trades[0][1] == null) {
        dic_trades[0][1] = 0
    } 

    Y_total_received.textContent = `${dic_trades[0][1]} ${dic_data[3]}`

    Y_exchangers.textContent = dic_trades[0][2]
    Y_date.textContent = dic_data[9]

    your_address.textContent  = dic_address[0]

    Y_coin_sender.textContent = dic_data[6]
    Y_coin_receive.textContent = dic_data[5]

    Y_min_value.textContent = `${dic_data[1]} ${dic_data[4]}`
    Y_max_value.textContent = `${dic_data[2]} ${dic_data[4]}`
    
    Y_trade_amount.textContent = `${dic_data[7]} ${dic_data[3]}`
}

function view_user_trade(data) {
    hideError()

    var dic_data = JSON.parse(data.response)
    var dic_address = JSON.parse(data.user_adress)

    var trade_id = JSON.parse(data.trade_id)

    var user_address = document.getElementById('user_address')
    
    var coin_sender = document.getElementById('coin_sender')
    var coin_receive = document.getElementById('coin_receive')

    var min_value = document.getElementById('min_value')
    var max_value = document.getElementById('max_value')

    var trade_amount = document.getElementById('trade_amount')

    user_address.textContent  = dic_address[0]

    coin_sender.textContent = dic_data[6]
    coin_receive.textContent = dic_data[5]

    min_value.textContent = `${dic_data[1]} ${dic_data[4]}`
    max_value.textContent = `${dic_data[2]} ${dic_data[4]}`
    
    trade_amount.textContent = `${dic_data[7]} ${dic_data[3]}`


    var estimated_value = document.getElementById('estimated_view')
    var amount_exchange = document.getElementById('amount_exchange')

    // Remove event listeners existentes
    var new_amount_exchange = amount_exchange.cloneNode(true);
    amount_exchange.replaceWith(new_amount_exchange);
    amount_exchange = new_amount_exchange;
    amount_exchange.value = ''
    estimated_value.textContent = ''

    amount_exchange.addEventListener('input', function(event) {
        amount_return = add_coin(amount_exchange.selectionStart, event.data, event.target.value, dic_data[6], 'sender_view', 10, 16)
       
        if (amount_return['senderValue']) {
            amount_exchange.value = amount_return['senderValue']
            return
        } else {
            amount_exchange.value = amount_return
        }

        if (amount_exchange.value != '') {
            socket.emit('estimulated_value', dic_data[6], amount_exchange.value.split(' ')[0], dic_data[5])
        } else {
            estimated_value.textContent = ''
        }
    }) 

    amount_exchange.addEventListener('keydown', (event) => {
        limit_keydown(amount_exchange, event)
    })
    
    socket.on('estimulated_value', (data) => {
        if (data.id) {
            hideError()
            showError(JSON.parse(data.response), JSON.parse(data.id), 16)   
        } else if (amount_exchange.value == '') {
            estimated_value.textContent = ''
        } else {
            estimated_value.textContent = `${JSON.parse(data.conversion)} ${dic_data[3]}`
        }
    }) 


    var submit_trade = document.getElementById('submit_trade')

    submit_trade.addEventListener('click', (event) => {
        var dic_send = {}

        dic_send['max_value'] = max_value.textContent.split(' ')[0]
        dic_send['min_value'] = min_value.textContent.split(' ')[0]

        dic_send['cripto_sender_id'] = coin_sender.textContent
        dic_send['cripto_recipient_id'] = coin_receive.textContent

        dic_send['amount_sender'] = amount_exchange.value.split(' ')[0]
        dic_send['amount_recipient'] = estimated_value.textContent.split(' ')[0]
        dic_send['reg_trade_id'] = trade_id

        socket.emit('update_trade', dic_send, user_address.textContent)
    })  

    socket.on('update_trade', (data) => {
        if (data.id) {
            hideError()
            showError(JSON.parse(data.response), JSON.parse(data.id), 18)   
        } else {    
            console.log('a')
        }
    }) 
}

var type_trade = null

function get_data_view(id_trade, type_modal) {
    type_trade = type_modal
    socket.emit('get_trade', id_trade, type_modal)
}

socket.on('get_trade', (data) => {
    if (type_trade == 'trade-details') {
        view_user_trade(data)
    } else {
        view_your_trade(data)
    }
})  
