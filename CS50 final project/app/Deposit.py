from flask import Flask, render_template, request, redirect, url_for

from models.crypto_data import CryptoInfo
import qrcode
import io
import base64
USER_ID = 1
app = Flask(__name__)

class Depositar:
    def __init__(self):
        self.data = CryptoInfo()

    #cria o qr code q leva pra /confirmation, onde o finaliza o deposito e redirecona pra pagina my_deposits
    def generate_confirmation_code(self):
        qr_data = url_for('confirm', _external=True)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        # Codifica a imagem como uma data URL
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        data_url = f"data:image/png;base64,{img_base64}"
        return data_url
    
    def deposit(self):
        currencies = ['USD']

        if request.method == 'POST':
            self.deposited_value = request.form.get('deposited_value')
            self.currency = request.form.get('currency')
            
            #verifica se a moeda ta certa
            if self.currency != 'USD':
                msg = 'Invalid currency'
                return render_template('deposit.html', currencies=currencies, msg=msg)
            
            tmp_value = []
            #verifica se o valor foi um valor numerico, se tiver letra ou outros caracteres n passa
            for digit in self.deposited_value:
                if digit.isdigit():
                    tmp_value.append(digit)

            tmp_value.insert(-2, ',')
            tmp_value_str = ''.join(tmp_value)

            if self.deposited_value != tmp_value_str:
                msg = 'Invalid value'
                return render_template('deposit.html', currencies=currencies, msg=msg)
            
            return True

depositar = Depositar()

@app.route('/deposit', methods=['GET', 'POST'])
def deposit_route():
    #se tiver tudo certo gera o qrcode e exibe pro usuario
    if depositar.deposit():
        qr_code_data_url = depositar.generate_confirmation_code()
        return render_template('deposit.html', currencies=['USD'], qr_code=qr_code_data_url)
    return render_template('deposit.html', currencies=['USD'])

@app.route('/confirm')
def confirm():
    depositar.data.set_deposit(USER_ID, depositar.deposited_value, depositar.currency)
    return redirect('my_deposits.html')
    #quando terminar volta pro dashboard com o poetru
if __name__ == '__main__':
    app.run(debug=True)
