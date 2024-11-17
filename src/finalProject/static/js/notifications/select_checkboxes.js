function allCheckbox(checkboxes_Send, actual_type, value_update=null) {
    var cond = true
    var checkboxes = checkboxes_Send

    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked == true && cond != false) {
            cond = true
        } else {
            cond = false
        }

    })

    checkboxes.forEach(function(checkbox) {

        if (cond == false) {
            checkbox.checked = true
        } else if (cond == true && value_update == null) {
            checkbox.checked = false
        }
    })


    if (value_update != null) {
        change_type_all(value_update, actual_type, checkboxes)
    }
}


function getVisibleCheckboxes() {
    var checkboxes = document.querySelectorAll('.checkbox');
    return Array.from(checkboxes).filter(function(checkbox) {
        return checkbox.offsetParent !== null;  // Verifica se o elemento está visível (presente no DOM)
    });
}


function selectCheckbox(checkboxes) {
    var selected = null;

    if (Array.isArray(checkboxes)) {
        selected = [];

        // Verifica quais estão selecionados
        checkboxes.forEach(function(checkbox) {
            if (checkbox.checked) {
                selected.push(checkbox.value);
            }
        });

        if (selected.length > 0) {
            return selected
        }
 
        return 'Error'
    }

    if (checkboxes instanceof HTMLInputElement && checkboxes.type === 'checkbox') {
        return checkboxes.value
    }

    return 'Error'
}
