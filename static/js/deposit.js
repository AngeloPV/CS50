document.getElementById('deposited_value').addEventListener('focus', function() {
    if (this.value === '0,00') {
       this.value = '';
    }
    });
    
    document.getElementById('deposited_value').addEventListener('blur', function() {
    let value = this.value;
    
    // Ve se ta vazio e coloca ,00 no fnal
    if (value === '') {
       this.value = '0,00';
    } else {
       // Se ja tiver a virgula
       if (value.includes(',')) {
           let parts = value.split(',');
    
           // Adiciona '0' se ja tiver 1 dígito após a vírgula
           if (parts[1].length === 1) {
               this.value = parts[0] + ',' + parts[1] + '0';
           } else if (parts[1].length === 0) {
               this.value = parts[0] + ',00';
           }
       } else {
           // Se não tiver vírgula, adiciona ',00'
           this.value = value + ',00';
       }
    }
});
    
    