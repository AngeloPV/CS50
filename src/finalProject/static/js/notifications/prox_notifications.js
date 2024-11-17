function prox_notifications(hidden) {

    var notifcationsProx = document.querySelectorAll('.notifcationsProx')
    var favoriteProx = document.querySelectorAll('.favoriteProx');
    var archiveProx = document.querySelectorAll('.archiveProx')
    var readProx = document.querySelectorAll('.readProx');
    var deleteButtons = document.querySelectorAll('.deleteButtons');

    // spread operator ... nodelist to array
    const allButtons = [...notifcationsProx, ...favoriteProx, ...archiveProx, ...readProx, ...deleteButtons]

    allButtons.forEach(button => {
        button.addEventListener('click', () => {
            var closest_section = button.closest('section');
            if (closest_section) {
                closest_section.classList.add('active_section');

                const div_notifications = document.querySelector('.notifications');
                div_notifications.classList.add('fade-out');

            } else {
                console.log('Nenhuma seção encontrada para o botão', button);
            }
        });
    });


    setTimeout(() => {

        deleteButtons.forEach(button => {
            button.addEventListener('click', function () {
                var closest_checkbox = button.closest('section').querySelector('.checkbox')
                var restult_closet = selectCheckbox(closest_checkbox);

                delete_notifications(restult_closet, hidden.value);
            });
        });


        archiveProx.forEach(button => {
            button.addEventListener('click', function () {
                var archive_checkbox = button.closest('section').querySelector('.checkbox')
                var archive_closet = selectCheckbox(archive_checkbox);

                change_type_all('archive', hidden.value, archive_closet)
            });
        });

        favoriteProx.forEach(button => {
            button.addEventListener('click', function () {
                var archive_checkbox = button.closest('section').querySelector('.checkbox')
                var archive_closet = selectCheckbox(archive_checkbox);

                change_type_all('favorite', hidden.value, archive_closet)
            });
        });


        notifcationsProx.forEach(button => {
            button.addEventListener('click', function () {
                var archive_checkbox = button.closest('section').querySelector('.checkbox')
                var archive_closet = selectCheckbox(archive_checkbox);

                change_type_all('standard', hidden.value, archive_closet)
            });
        });


        readProx.forEach(button => {
            button.addEventListener('click', function () {
                var archive_checkbox = button.closest('section').querySelector('.checkbox')
                var archive_closet = selectCheckbox(archive_checkbox);
                
                change_type_all(0, hidden.value, archive_closet)
            });
        });
    }, 500); // Tempo que deve ser igual ao tempo da animação
}
