function add_trade() {
    var btn_submit = document.getElementById('add_trade')
    var dic_values = {}


    var sender = document.getElementById('sender')
    dic_values['cripto_sender_id'] = sender.options[sender.selectedIndex].value

    var amount_sender = document.getElementById('amount-sender')
    var estimated_value = document.getElementById('estimated_value')

    
    var receive = document.getElementById('receive')
    dic_values['cripto_recepient_id'] = receive.options[receive.selectedIndex].value;

    var amount_min = document.getElementById('minimum_value') 


    receive.addEventListener('change', function(event) {
        dic_values['cripto_recepient_id'] = event.target.value
  
        var change_coin = null

        if (amount_min.value != '') {  
            change_coin = amount_min.value.split(' ')     
            amount_min.value = `${change_coin[0]} ${dic_values['cripto_recepient_id']}`
        }
        
        if (amount_sender.value.split(' ')[0]) {
            socket.emit('estimulated_value', dic_values['cripto_sender_id'], amount_sender.value.split(' ')[0], dic_values['cripto_recepient_id'])
        }
    })

    sender.addEventListener('change', function(event) {
        dic_values['cripto_sender_id'] = event.target.value

        var change_coin = null

        if (amount_sender.value != '') {  
            change_coin = amount_sender.value.split(' ')     
            amount_sender.value = `${change_coin[0]} ${dic_values['cripto_sender_id']}`
        }

        if (change_coin != null && dic_values['cripto_recepient_id'] != 'Select') {
            socket.emit('estimulated_value', dic_values['cripto_sender_id'], change_coin[0], dic_values['cripto_recepient_id'])
        } 
    })


    amount_sender.addEventListener('input', function(event) {
        amount_return = add_coin(amount_sender.selectionStart, event.data, event.target.value, dic_values['cripto_sender_id'], 
            'cripto_sender', 10, true)
        
        if (amount_return['senderValue']) {
            amount_sender.value = amount_return['senderValue']
            return
        } else {
            amount_sender.value = amount_return
        }
        
        if (amount_return['error']) {
            return
        }

  
        if (amount_sender.value !== '' && dic_values['cripto_sender_id'] != 'Select' && dic_values['cripto_recepient_id'] != 'Select' && 
            dic_values['cripto_recepient_id'] != dic_values['cripto_sender_id']) {
            console.log('aa')
            socket.emit('estimulated_value', dic_values['cripto_sender_id'], amount_sender.value.split(' ')[0], dic_values['cripto_recepient_id'])
        } else {
            estimated_value.value = ''
        }
    })

    amount_sender.addEventListener('keydown', (event) => {
        limit_keydown(amount_sender, event)
    })


    amount_min.addEventListener('input', function(event) {
        amount_return = add_coin(amount_min.selectionStart, event.data, event.target.value, dic_values['cripto_recepient_id'], 'cripto_receive', 
            10, true)
       
        if (amount_return['senderValue']) {
            amount_min.value = amount_return['senderValue']
            return
        } else {
            amount_min.value = amount_return
        }
    })

    amount_min.addEventListener('keydown', (event) => {
        limit_keydown(amount_min, event)
    })

    

    btn_submit.addEventListener('click', () => {
        let password = document.querySelector('.input-field').value
        dic_values['amount_max'] = document.getElementById('estimated_value').value.split(' ')[0]
        dic_values['amount_min'] = amount_min.value.split(' ')[0]
        dic_values['amount_cripto_sender'] = amount_sender.value.split(' ')[0]

        socket.emit('add_trade', dic_values, password)
    })


    socket.on('estimulated_value', (data) => {
        if (data.id) {
            hideError()
            showError(JSON.parse(data.response), JSON.parse(data.id), true)   
        } else if (amount_sender.value.trim() === '') {
            estimated_value.value = ''
        } else {
            hideError()

            estimated_value.value = `${JSON.parse(data.conversion)} ${JSON.parse(data.back_coin)}`
        }
    })


    socket.on('add_trade', (data) => {
        if (data.id) {
            hideError()
            showError(JSON.parse(data.response), JSON.parse(data.id), true)   
        } else {
            hideError()

            var get_modal = document.getElementById('add-trade')
            get_modal.style.display = 'none'

            showCustomAlert(
                '.modal',
                'Account Verified Successfully',
                '<p>Trade added successfully!</p>',
                'success',
                'Continue',
                ["custom-title_sucess", "custom-succes-button"]
            );

            var get_trades = document.getElementById('your_trades')
        
            send_change(get_trades)
        }
    })
}

