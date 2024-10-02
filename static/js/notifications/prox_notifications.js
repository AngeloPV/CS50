function prox_notifications(hidden) {
    var deleteButtons = document.querySelectorAll('.deleteButtons');

    var deleteButtons = document.querySelectorAll('.deleteButtons');
    deleteButtons.forEach(button => {
        button.replaceWith(button.cloneNode(true));  // Remove listeners antigos
    });

    var deleteButtons = document.querySelectorAll('.deleteButtons');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            var closest_checkbox = button.closest('tr').querySelector('.checkbox')
            var restult_closet = selectCheckbox(closest_checkbox);
            // console.log(hidden.value)

            delete_notifications(restult_closet, hidden.value);
        });
    });


    var archivrProx = document.querySelectorAll('.archivrProx')
    var archivrProx = document.querySelectorAll('.archivrProx');
    archivrProx.forEach(button => {
        button.replaceWith(button.cloneNode(true));  // Remove listeners antigos
    });

    var archivrProx = document.querySelectorAll('.archivrProx');
    archivrProx.forEach(button => {
        button.addEventListener('click', function () {
            var archive_checkbox = button.closest('tr').querySelector('.checkbox')
            var archive_closet = selectCheckbox(archive_checkbox);
            
            console.log(hidden);
            console.log(archive_closet)

            change_type_all('archive', hidden.value, archive_closet)
        });
    });


    var favoriteProx = document.querySelectorAll('.favoriteProx')
    var favoriteProx = document.querySelectorAll('.favoriteProx');
    favoriteProx.forEach(button => {
        button.replaceWith(button.cloneNode(true));  // Remove listeners antigos
    });

    var favoriteProx = document.querySelectorAll('.favoriteProx');
    favoriteProx.forEach(button => {
        button.addEventListener('click', function () {
            var archive_checkbox = button.closest('tr').querySelector('.checkbox')
            var archive_closet = selectCheckbox(archive_checkbox);
            
            console.log(hidden);
            console.log(archive_closet)

            change_type_all('favorite', hidden.value, archive_closet)
        });
    });


    var notifcationsProx = document.querySelectorAll('.notifcationsProx')
    var notifcationsProx = document.querySelectorAll('.notifcationsProx');
    notifcationsProx.forEach(button => {
        button.replaceWith(button.cloneNode(true));  // Remove listeners antigos
    });

    var notifcationsProx = document.querySelectorAll('.notifcationsProx');
    notifcationsProx.forEach(button => {
        button.addEventListener('click', function () {
            var archive_checkbox = button.closest('tr').querySelector('.checkbox')
            var archive_closet = selectCheckbox(archive_checkbox);
            
            console.log(hidden);
            console.log(archive_closet)

            change_type_all('standard', hidden.value, archive_closet)
        });
    });


    var readProx = document.querySelectorAll('.readProx')
    var readProx = document.querySelectorAll('.readProx');
    readProx.forEach(button => {
        button.replaceWith(button.cloneNode(true));  // Remove listeners antigos
    });

    var readProx = document.querySelectorAll('.readProx');
    readProx.forEach(button => {
        button.addEventListener('click', function () {
            var archive_checkbox = button.closest('tr').querySelector('.checkbox')
            var archive_closet = selectCheckbox(archive_checkbox);
            

            change_type_all(0, hidden.value, archive_closet)
        });
    });
}