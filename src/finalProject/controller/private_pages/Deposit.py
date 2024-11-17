from flask import request, redirect, session, url_for
from ...models.Deposit_data import Deposit_data
from ...renderer import template_render
import qrcode # type: ignore
import io
import base64

USER_ID = session.get('user_id')


class Deposit:
    def __init__(self):
        self.data = Deposit_data()

    #cria o qr code q leva pra /confirmation, onde o finaliza o deposito e redirecona pra pagina my_deposits
    def generate_confirmation_code(self):
        qr_data = redirect('deposit/confirm')
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='#f8f9fa')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        # Codifica a imagem como uma data URL
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        data_url = f"data:image/png;base64,{img_base64}"
        return data_url
    
    def index(self):
        #se tiver tudo certo gera o qrcode e exibe pro usuario
        currencies = ['USD']

        if request.method == 'POST':

            deposited_value = request.form.get('deposited_value')
            currency = request.form.get('currency')

            #verifica se a moeda ta certa
            if currency != 'USD':
                msg = 'Invalid currency'
                data = {
                "currencies": currencies, "error_message":msg
                }
                return template_render('deposit.html', **data)
            
            tmp_value = []
            #verifica se o valor foi um valor numerico, se tiver letra ou outros caracteres n passa
            for digit in deposited_value:
                if digit.isdigit():
                    tmp_value.append(digit)

            tmp_value.insert(-2, ',')
            tmp_value_str = ''.join(tmp_value)

            if deposited_value != tmp_value_str:
                msg = 'Invalid value'
                data = {
                "currencies": currencies, "error_message":msg
                }
                return template_render('deposit.html', **data)
            
            #verifica se o valor é menor q 1
            if float(deposited_value.replace(',', '.')) < 1:
                msg = 'Minimum deposit is $1'
                data = {
                "currencies": currencies, "error_message":msg
                }
                return template_render('deposit.html', **data)

            #salva os valores nos atributos
            session['deposited_value'] = deposited_value
            session['currency'] = currency
            # apos todas as etapas de verificacao gera o qrcode
            qr_code_data_url = self.generate_confirmation_code()
            data = {
                "currencies": currencies, "qr_code":qr_code_data_url, "deposited_value": session['deposited_value'], 
                "currency_selected":session['currency']
                }
            return template_render('deposit.html', **data)
        data = {"currencies": currencies,}
        return template_render('deposit.html', **data)
    
    def confirm(self):

        if request.method == 'GET':

            deposited_value = session.get('deposited_value')
            currency = session.get('currency')

            data = {
                "deposited_value": deposited_value, "currency":currency
            }
            return template_render('deposit_confirm.html', **data)
        
        if request.method == 'POST':
            if request.form.get('button'):
                self.data.set_deposit(USER_ID, session.get('deposited_value'), session.get('currency'))

                #Limpa a session deposited_value e currency
                session.pop('deposited_value', None)
                session.pop('currency', None)
                return redirect(url_for("main_routes.route_method", route_name="my_deposits", method="index"))
            
