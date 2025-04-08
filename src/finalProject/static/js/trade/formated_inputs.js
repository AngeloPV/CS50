function formarted_input(value, dic_camp, elementId=null, limit_input, margin_bottom) {
    var senderValue = value.trim()
    
    var parts = senderValue.split('.')
    var verify = false
    if (!senderValue.includes('.') && senderValue.length > limit_input) {
        senderValue = senderValue.slice(0, limit_input) + '.' + senderValue.slice(limit_input)
        parts = senderValue.split('.');
    }

    if (parts[0].length > limit_input) {
        parts[0] = parts[0].slice(0, limit_input);
    }

    if (parts.length > 1) {
        var decimalPart = parts[1];
        if (decimalPart.length > 3 && value != null) {
            hideError()

            var camp_text = `*You only can have ${limit_input} integers and 3 decimal numbers!`
            var camp_id = elementId 
            showError(camp_text, camp_id, margin_bottom)
            
            decimalPart = decimalPart.slice(0, 3)
            verify = true
        }
        senderValue = parts[0] + '.' + decimalPart
    } else {
        senderValue = parts[0]
    }

    if (dic_camp == 'Select') {
        return senderValue
    }

    if (verify) {
        return_data = {senderValue: `${senderValue} ${dic_camp}`, error: verify}
        return return_data
    }

    return `${senderValue} ${dic_camp}`
}



function add_coin(cursor_position, lastData, senderValue, dic_camp, elementId, limit_input=10, margin_bottom=false){
    hideError()

    let lastValue = lastData

    var change_coin = senderValue.split(' ')


    var parts = change_coin[0].split('.');

    if (parts.length > 1) {
        var camp_text =`*You only can have ${limit_input} integers and 3 decimal numbers!`
        var camp_id = elementId;

        if (parts[0].length > limit_input) {

            change_coin[0] = change_coin[0].slice(0, cursor_position - 1) + change_coin[0].slice(cursor_position);
            showError(camp_text, camp_id, margin_bottom)
       
        } else if (parts[1].length > 3) {
            change_coin[0] = change_coin[0].slice(0, cursor_position - 1) + change_coin[0].slice(cursor_position);
            showError(camp_text, camp_id, margin_bottom)
        }
    }


    if (!change_coin[0]) {
        return ''
    }

    if (change_coin[1]) {
        if(lastValue == null && cursor_position > change_coin[0].length) {
            console.log('a')
            change_coin[0] = change_coin[0].slice(0, -1)
        } else if (cursor_position > change_coin[0].length) {
            change_coin[0] = `${change_coin[0]}${lastValue}` 
        }

        if (change_coin[0] != '') {
            senderValue = change_coin[0]

        } else {
            senderValue = ''
            return senderValue
        }

    } else if ((change_coin[0].includes('Bitcoin') || change_coin[0].includes('Ethereum')) && lastData == null)  {
        var onlyNumbers = change_coin[0].match(/^\d+/)[0];
        onlyNumbers = onlyNumbers.slice(0, -1)
       
        senderValue = onlyNumbers
    } else  {
        senderValue = senderValue
    }


    return formarted_input(senderValue, dic_camp, elementId, limit_input, margin_bottom)
}


function limit_keydown(input, event) {
    if (!((event.key >= '0' && event.key <= '9') || event.key === 'Backspace' || event.key === 'Delete' || event.key === 'ArrowLeft' ||             
        event.key === 'ArrowRight' || (event.key === '.' && !input.value.includes('.')))){
        event.preventDefault();
      }
}