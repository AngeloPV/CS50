from flask import request, redirect, session, url_for
from ...models.Deposit_data import Deposit_data
from ...models.User import User
from ...renderer import template_render
import qrcode # type: ignore
import io
import base64

USER_ID = session.get('user_id')

class Deposit:
    """
    Classe responsavel por validar os dados e realizar o depósito
    """
    def __init__(self):
        self.data = Deposit_data() #intancia a classe responsavel pelos dados do deposito
        self.user_data = User() #intancia a classe responsavel pelos dados do usuario

    #cria o qr code q leva pra /confirmation, onde o finaliza o deposito e redirecona pra pagina my_deposits
    def generate_confirmation_code(self):
        """
        Cria um qr code que será exibido após o usuário digitar o valor do depósito e levará para a página
        de confirmação onde será realmente efetivado e depositado na conta do usuario
        """

        #link para onde o qr code irá levar
        qr_data = redirect('deposit/confirm')
        
        #gera o qr code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        #gera a imagem do qr code com o preenchimento branco e a cor de fundo do modal
        img = qr.make_image(fill='black', back_color='#f8f9fa')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        # codifica a imagem como uma data URL e a retorna
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        data_url = f"data:image/png;base64,{img_base64}"
        return data_url
    
    def index(self):
        """
        Renderiza a pagina de depósito onde o usuario irá selecionar o valor a ser depositado e a moeda
        """
        # Limpa o valor authorize, que foi usado para exibir um sweet alert de confirmação do deposito
        if 'authorize' in session:
            del session['authorize']

        # Salva as moedas disponíveis
        currencies = ['USD']

        if request.method == 'POST':
            #pega os dados do formulario
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

            #formatando o valor
            tmp_value.insert(-2, ',')
            tmp_value_str = ''.join(tmp_value)

            #verifica se o valor é  valido
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

            #gera a data com o qr_code e retorna paga a pagina Deposit onde será exibido o qr code para o usuario
            data = {
                "currencies": currencies, "qr_code":qr_code_data_url, "deposited_value": session['deposited_value'], 
                "currency_selected":session['currency']
                }
            return template_render('deposit.html', **data)
        
        #Carrega a página com as moedas
        data = {"currencies": currencies,}
        return template_render('deposit.html', **data)
    
    def confirm(self):
        """
        Renderiza a página de confirmação que será acessada após o qr code ser lido, é aqui onde o depósito
        será efetivado
        """
        if request.method == 'GET':
            #Pega o valor depositado e a moeda pela sessao
            deposited_value = session.get('deposited_value')
            currency = session.get('currency')

            #retorna esses dados para a pagina de confirmação
            data = {
                "deposited_value": deposited_value, "currency":currency
            }
            return template_render('deposit_confirm.html', **data)
        
        #Verifica se o formulario foi enviado
        if request.method == 'POST':
            if request.form.get('button'):
                #Efetua o depósito
                self.data.set_deposit(USER_ID, session.get('deposited_value'), session.get('currency'))
                self.user_data.update_cash(sit='+', user_id=USER_ID, cash=session.get('deposited_value'))

                #atualiza o saldo
                session['balance'] = self.user_data.get_cash(user_id=session.get('user_id'))

                #Limpa a session deposited_value e currency
                session.pop('deposited_value', None)
                session.pop('currency', None)

                #Retorna o authorize que será usado para exibir um sweet alert de confirmação
                data = {'authorize': 'Deposit finished successfully!', 'redirect_url': '/my_deposits/index'}
                return template_render("deposit_confirm.html", **data)
            
