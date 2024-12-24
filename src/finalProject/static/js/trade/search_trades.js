function search_trades() {
    var btn_search = document.getElementById('search_trade')
    var dic_search = {}


    var search_sender = document.getElementById('search_sender')
    dic_search['search_sender'] = search_sender.options[search_sender.selectedIndex].value

    var search_maximum = document.getElementById('search_maximum')
    var search_minumum = document.getElementById('search_minumum')

    search_sender.addEventListener('change', function(event) {
        hideError()

        dic_search['search_sender'] = event.target.value

        var change_coin = null

        if (search_maximum.value != '') {       
            change_coin = search_maximum.value.split(' ')     
            search_maximum.value = `${change_coin[0]} ${dic_search['search_sender']}`
        }

        if (search_minumum.value != '') {       
            change_coin = search_minumum.value.split(' ')     
            search_minumum.value = `${change_coin[0]} ${dic_search['search_sender']}`
        }

    })

    search_maximum.addEventListener('input', function(event) {
        maximum_return = add_coin(search_maximum.selectionStart, event.data, event.target.value, dic_search['search_sender'], 
            'search_error', 12, true)

        if (maximum_return['senderValue']) {
            search_maximum.value = maximum_return['senderValue']
            return
        } else {
            search_maximum.value = maximum_return
        }
    })  

    search_maximum.addEventListener('keydown', (event) => {
        limit_keydown(search_maximum, event)
    })
 
    search_minumum.addEventListener('input', function(event) {
        minumum_return = add_coin(search_minumum.selectionStart, event.data, event.target.value, dic_search['search_sender'], 
            'search_error', 12, true)

        if (minumum_return['senderValue']) {
            search_minumum.value = minumum_return['senderValue']
            return
        } else {
            search_minumum.value = minumum_return
        }
    })

    search_minumum.addEventListener('keydown', (event) => {
        limit_keydown(search_minumum, event)
    })

    btn_search.addEventListener('click', () => {
        let tradeType = document.querySelector('input[name="trade_type"]:checked').value;
        dic_search['amount_max'] = search_maximum.value.split(' ')[0]
        dic_search['amount_min'] = search_minumum.value.split(' ')[0]

        socket.emit('search_trade', dic_search, tradeType)
    })


    socket.on('search_trade', (data) => {
        var container = document.getElementById('search_container')

        if (data.id) {
            container.style.marginBottom = "10px";

            hideError()
            showError(JSON.parse(data.response), JSON.parse(data.id), true) 
        } else {
            container.style.marginBottom = "30px";
            hideError()
            
            var your_trades = document.getElementById('your_trades');

            // Voltar à lista correta de trades (não trocar enquanto a ação estiver em andamento)

            var type = null

            if (data.condition) {
                your_trades.textContent = "";
                your_trades.innerHTML += "<i class='fa-solid fa-backward'></i> Return";
                type = 'your_trade'
            } else {
                your_trades.textContent = "";
                your_trades.innerHTML += "<i class='fa-solid fa-eye'></i> Your Trades";
                type = 'all_trade'
            }


            change_html(data, type)
        }
    })
}