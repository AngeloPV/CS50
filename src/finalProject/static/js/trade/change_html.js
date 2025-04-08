function change_html(data, type) {
    const receivedData = JSON.parse(data.data)


    var main_html = document.querySelector(".trade-grid")

    // Verify if exist 
    if (!Array.isArray(receivedData) || receivedData == null || receivedData.length === 0) {
        console.log("Nenhuma trade disponível.");
        
        main_html.innerHTML = ''
        
        return;
    }

    main_html.innerHTML = ''

    receivedData.forEach(row => {
        let newRow
        
        newRow = `<section class="trade-card ${row[5]}">`
        
        if (type == 'checkbox') {
            newRow += `<input value='${row[8]}' type="checkbox" class="checkbox" />`
        }
        else if (type == 'your_trade') {
            hideDeleteSection() 
            newRow += '<span class="status">Your Trade</span>'
        }else {
            hideDeleteSection() 
            newRow += '<span class="status">Disponível</span>'
        }

        if (row[3] == "BTC") {
            newRow += `<h2><i class="fa-brands fa-bitcoin" style="color: #ff6f3c;"></i>${row[5]}</h2>`
        } else { 
            newRow += `<h2><i class="fa-brands fa-ethereum" style="color: #1B263B"></i>Ethereum</h2>`
        }
        newRow +=
            `<hr>

            <div class="trade-info">
                <p><i class="fas fa-coins"></i><b>Value offered</b> ${row[7]} ${row[3]}</p>
                <p><i class="fa-solid fa-dollar-sign"></i><b>Greater value:</b> ${row[2]} ${row[4]}</p>
                <p><i class="fa-solid fa-dollar-sign"></i><b>Lowest value:</b> ${row[1]} ${row[4]}</p>
            </div>`

        if (type == 'your_trade') {
            newRow += `<button value="${row[8]}" class="open_modal button" data-modal="y_trade-details">Ver mais</button>`
        } else {
            newRow += `<button value="${row[8]}" class="open_modal button" data-modal="trade-details">Ver mais</button>`
        }
        
        newRow += `</section>`

        main_html.innerHTML += newRow

    })

    open_modals()
}