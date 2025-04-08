from flask import request, session, redirect, url_for
import re
from ...renderer import template_render
from ...helper.helper_select import Select
from ...helper.helper_update import Update
from ...helper.send_email import Send_Email 
from ...helper.valitade import Validate
from ...helper.postal_code import Postal_code

from ...models.Authenticate_account_user import Authenticate_account_user
from ...models.User import User

from datetime import datetime 

class Account:
    """
    Classe responsavel pelo gerenciamente das informações do usuario e suas preferencias
    """
    def __init__(self):
        self.valitade = Validate() #cria uma instancia responsavel pela validação
        self.select = Select() #cria uma instancia responsavel pra resgatar dados do banco
        self.update = Update() #cria uma instancia responsavel pra atualizar dados do banco
        self.send_email = Send_Email() #cria uma instancia responsavel pra enviar emails
        self.authenticate = Authenticate_account_user() #cria uma instancia responsavel por autenticar o usuário
        self.postal_code = Postal_code() #cria uma instancia responsavel por pegar a localização do usuário
        self.user = User() #cria uma instancia responsavel por pegar as informações do usuário

    def do_email_send(self, to_update):
        """
        Função responsavel por enviar um email para o usuario, pegando os dados necessários do banco e
        trazendo para a função que send_email(config_email) para criar o email com as informações do usuario
        """
        self.select.exe_select("SELECT id, name, email FROM user_data where id = %s LIMIT %s", f'{{"id": "{session["user_id"]}", "LIMIT": "1"}}') 
        email_data = self.select.get_result()


        date_day = int(datetime.now().day) + 1 
        

        if email_data:
                email_data = {"id": email_data[0], "name": email_data[1], "verify": date_day, "email": email_data[2]}
                url = "account/verify/"

                if self.send_email.config_email(2, email_data, url, type='code', to_update=to_update):
                    #pega o código gerado e armazena na sessao
                    session['code'] = self.send_email.get_code()
                    
                    return True, template_render('verify.html')
                data = {'msg': "Email não existe, email invalido, email n reconhecido, email de 4"}\
                
        data = {'msg': "Erro ao enviar email"}
        return False,data
                
    def validate_data(self, to_update=''):
         """
         Realiza a validação da senha inserida pelo usuario após selecionar pra alterar os dados,
         caso a senha seja valida, retorna a funcao do_email_send
         """
         if request.method == 'POST':
            #pega a senha
            user_password = request.form.get('password')

            #verifica se a senha está no padrão adequado
            if not self.valitade.validate_password(user_password):
                data = {'msg': session.get("error_validate")}

                return False, data

        
            #pega a senha do usuario no banco
            self.select.exe_select("SELECT password FROM user_data WHERE id = %s LIMIT %s", f'{{"id": "{session["user_id"]}", "LIMIT": "1"}}')
            db_password = self.select.get_result()

            #verifica se a senha digitada é a mesma que a do usuário
            if not self.valitade.encryption(user_password, *db_password):
                data = {'msg': session.get("error_validate")}

                return False, data
            
            #retorna a função do_email_send 
            return self.do_email_send(to_update=to_update)
              
    def index(self):
        """
        Renderiza a página com todas as informações do usuário e suas preferencias para que possam 
        posteriormente serem alteradas pelo mesmo
        """
        name = self.user.get_user_name(user_id=session.get('user_id'))
        email = self.user.get_user_email(user_id=session.get('user_id'))
        phone = self.user.get_user_phone(user_id=session.get('user_id'))
        #user locate returna {'city': 'cidade', 'state': 'estado', 'country': 'pais'}
        user_locate = self.postal_code.get_city_state_country(self.user.get_postal_code(user_id=session.get('user_id')))
        if user_locate:
            user_locate['cep'] = self.user.get_postal_code(user_id=session.get('user_id'))
       
        #data padrao
        data = {
            'name': name,
            'first_name': name[0],
            'last_name': name[-1],
            'email': email,
            'phone': phone
        }

        # adiciona os campos de localização apenas se user_locate for válido
        if user_locate:
            data.update({
                'city': user_locate.get('cidade'),
                'state': user_locate.get('estado'),
                'country': user_locate.get('pais'),
                'postal_code': user_locate.get('cep')
            })
        
        # Remove o campo ' a ser atualizado' da sessao
        if 'to_update' in session:
            del session['to_update']


       # Pega os dados ad url
        authorize = request.args.get('authorize') #exibe um sweet alert de confirmacao
        redirect_url = request.args.get('redirect_url') #url para o Account
        if authorize:
            data['authorize'] = authorize
        if redirect_url:
            data['redirect_url'] = redirect_url
        return template_render('account.html', **data)
    

    
    def phone(self):
        """
        A lógica de todas as funções responsaveis por alterar os dados do usuario seguem a mesma desta 
        funcao
        """
        if request.method == 'POST':
            #2° Parte
            #apos digitar o codigo corretamente a pagina vai atualizar e vai pedir o dado a ser alterado
            #e a confirmação do mesmo, se estiver tudo correto, altera os dados, senao, retorna erro
            if request.form.get('update_send_button'):
                phone = str(request.form.get('phone'))
                confirm_phone = str(request.form.get('confirm_phone'))

                #tratamento dos dados
                phone = phone.strip() #tira os espaços
                confirm_phone = confirm_phone.strip() 

                #tira os parenteses pra fazer a verificacao
                phone = phone.replace("(", "").replace(")", "")
                confirm_phone = confirm_phone.replace("(", "").replace(")", "")

                #verifica se ambos estao no modelo: (12)123456789
                if not self.valitade.validate_phone(phone) or not self.valitade.validate_phone(confirm_phone):
                    data = {'msg': 'Invalid phone number', "verified": True, "to_update": f'{session.get("to_update")}'}
                    # print(phone, confirm_phone)
                    return template_render("update_data.html", **data)
                
                #adiciona os paranteses novamente
                phone = f"({phone[:2]}){phone[2:]}"
                confirm_phone = f"({confirm_phone[:2]}){confirm_phone[2:]}"

                #verifica se ambos sao iguais
                if not phone == confirm_phone:
                    data = {'msg': 'Fields must be the same', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
                #Após tudo verificado, será feito a atualização dos dados
                self.update.exe_update(data={"phone": f"{phone}"}, table_name='user_data', 
                                       data_where={'id': f'{session.get("user_id")}'}, operator='=, =')
                
                
                data = {'authorize': 'Phone updated successfully!', 'redirect_url': '/account/index'}
                return redirect(url_for("main_routes.route_method", route_name="account", method='index', **data))


            #1°parte
            #Valida a senha digitada
            result = self.validate_data('phone')

            #caso a validação falhe, retorna a pagina com a msg armazenada em result[1]
            if not result[0]:
                data = result[1]
                return template_render("update_data.html", **data) 
            
            #passa oq o usuario vai alterar pela sessao e leva para a pagina Verify onde será requirido
            #um codigo de confirmação enviado pelo email, caso digite corretamente, vai para a 
            #2° parte(linha 121)
            session['to_update'] = 'phone'  
            return template_render('verify.html') 
            
        return template_render('update_data.html')
    
    def email(self):
        if request.method == 'POST':
            #2°parte
            if request.form.get('update_send_button'):
                email = str(request.form.get('email'))
                confirm_email = str(request.form.get('confirm_email'))  

                #verifica se o email é valido
                if not self.valitade.validate_email(email, False) or not self.valitade.validate_email(confirm_email, False):
                    data = {'msg': 'invalid email', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
            
                #verifica se ambos sao iguais
                if not email == confirm_email:
                    data = {'msg': 'Fields must be the same', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)

                self.update.exe_update(data={"email": f"{email}"}, table_name='user_data', 
                                       data_where={'id': f'{session.get("user_id")}'}, operator='=, =')
                
                
                data = {'authorize': 'Email updated successfully!', 'redirect_url': url_for("main_routes.route_method", route_name="account", method="index")}
                return redirect(url_for("main_routes.route_method", route_name="account", method='index', **data))

            #1°parte
            result = self.validate_data('email')
            if not result[0]:
                data = result[1]
                return template_render("update_data.html", **data) 
            #passa oq o usuario vai alterar pela sessao
            session['to_update'] = 'email'  
            return template_render('verify.html') 

        return template_render('update_data.html')
    
    def password(self):
        if request.method == 'POST':
            #2°parte
            if request.form.get('update_send_button'):
                password = str(request.form.get('password'))
                confirm_password = str(request.form.get('confirm_password')) 

                #valida a senha para ver se esta no formato adequado
                if not self.valitade.validate_password(password) or not self.valitade.validate_password(confirm_password):
                    data = {'msg': 'Invalid password', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
                #verifica se ambos sao iguais
                if not password == confirm_password:
                    data = {'msg': 'Fields must be the same', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
                #verifica se a senha digitada é coerente com a do banco
                encrypted_password = self.valitade.encryption(password)
                self.update.exe_update(data={"password": f"{encrypted_password}"}, table_name='user_data', 
                                       data_where={'id': f'{session.get("user_id")}'}, operator='=, =')
                
              
                data = {'authorize': 'Password updated successfully!', 'redirect_url': url_for("main_routes.route_method", route_name="account", method="index")}
                return redirect(url_for("main_routes.route_method", route_name="account", method='index', **data))
        
        #1°parte
            result = self.validate_data('password')
            if not result[0]:
                data = result[1]
                return template_render("update_data.html", **data) 
            #passa oq o usuario vai alterar pela sessao
            session['to_update'] = 'password'  
            return template_render('verify.html') 

        return template_render('update_data.html')
        
    def name(self):
        if request.method == 'POST':
            if request.form.get('update_send_button'):
                name = str(request.form.get('name'))
                confirm_name = str(request.form.get('confirm_name'))
                
                #verifica se tem algum numero no meio dos nomes
                if any(char.isdigit() for char in name) or any(char.isdigit() for char in confirm_name):
                    data = {'msg': 'Enter a valid name', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                #verifica se os nomes sao iguais
                if not name.lower() == confirm_name.lower():
                    data = {'msg': 'Fields must be equal', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
                #se tudo der certo atualiza os dados
                self.update.exe_update(data={"name": f"{name.title()}"}, table_name='user_data', 
                                       data_where={'id': f'{session.get("user_id")}'}, operator='=, =')
             
                data = {'authorize': 'Name updated successfully!', 'redirect_url': url_for("main_routes.route_method", route_name="account", method="index")}
                return redirect(url_for("main_routes.route_method", route_name="account", method='index', **data))

            result = self.validate_data('user name')
            if not result[0]:
                data = result[1]
                return template_render("update_data.html", **data) 
            #passa oq o usuario vai alterar pela sessao
            session['to_update'] = 'name'  
            return template_render('verify.html') 

        return template_render('update_data.html')
    
    def cep(self):
        if request.method == 'POST':
            if request.form.get('update_send_button'):
                cep = str(request.form.get('cep'))
                confirm_cep = str(request.form.get('confirm_cep'))

                if not cep or not confirm_cep:
                    data = {'msg': 'All fields must be filled out', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
                #verifica se tem algum numero no meio dos nomes
                if not self.postal_code.is_valid_zip_code(cep):
                    data = {'msg': 'Enter a valid postal code', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                #verifica se os nomes sao iguais
                if not cep == confirm_cep:
                    data = {'msg': 'Fields must be the same', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
               
                #formata o CEP removendo qualquer caractere que não seja número
                cep = re.sub(r"\D", "", cep) 

                #formata o cep novamente pra ficar no modelo 00000-000
                if not '-' in cep:
                    cep = f"{cep[:5]}-{cep[5:]}"

                #se tudo der certo atualiza os dados
                self.update.exe_update(data={"cep": f"{cep}"}, table_name='user_data', 
                                       data_where={'id': f'{session.get("user_id")}'}, operator='=, =')
              
                data = {'authorize': 'Postal code updated successfully!', 'redirect_url': url_for("main_routes.route_method", route_name="account", method="index")}
                return redirect(url_for("main_routes.route_method", route_name="account", method='index', **data))

            result = self.validate_data('cep')
            if not result[0]:
                data = result[1]
                return template_render("update_data.html", **data) 
            #passa oq o usuario vai alterar pela sessao
            session['to_update'] = 'cep'  
            return template_render('verify.html') 

        return template_render('update_data.html')