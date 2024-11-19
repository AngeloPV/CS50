from flask import request, session, redirect, url_for
from ...renderer import template_render
from ...helper.helper_select import Select
from ...helper.helper_update import Update
from ...helper.send_email import Send_Email 
from ...helper.valitade import Validate
from ..protected_pages.user_data import User_data

from ...models.Authenticate_account_user import Authenticate_account_user

from datetime import datetime 

class Account:
    def __init__(self):
        self.valitade = Validate()
        self.select = Select()
        self.update = Update()
        self.send_email = Send_Email()
        self.user_data = User_data()
        self.authenticate = Authenticate_account_user()

    def do_email_send(self):
        self.select.exe_select("SELECT id, name, email FROM user_data where id = %s LIMIT %s", f'{{"id": "{session["user_id"]}", "LIMIT": "1"}}') 
        email_data = self.select.get_result()


        date_day = int(datetime.now().day) + 1 
        

        if email_data:
                email_data = {"id": email_data[0], "name": email_data[1], "verify": date_day, "email": email_data[2]}
                url = "account/verify/"

                if self.send_email.config_email(2, email_data, url, type='code'):
                    #pega o código gerado e armazena na sessao
                    session['code'] = self.send_email.get_code()
                    
                    return True, template_render('verify.html')
                data = {'msg': "Email não existe, email invalido, email n reconhecido, email de 4"}\
                
        data = {'msg': "Erro ao enviar email"}
        return False,data
                
    def validate_data(self):
         if request.method == 'POST':
            #pga a senha
            user_password = request.form.get('password')

            #verifica se a senha está no padrão adequado
            if not self.valitade.valitdate_password(user_password):
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
            return self.do_email_send()
              
    def index(self):
        name = self.user_data.get_user_name(user_id=session.get('user_id'))
        email = self.user_data.get_user_email(user_id=session.get('user_id'))
        phone = self.user_data.get_user_phone(user_id=session.get('user_id'))

        data = {'name': name,
                'first_name': name[0], 
                'last_name': name[-1],
                'email': email, 
                'phone': phone, 
                }
        return template_render('account.html', **data)
    

    
    #valida as informaçoes e armazena em result, se for false, retorna a pagina com a msg armzenada em result[1]
    #se for true, armazena o dado a ser alterado na sessao e retorna o verify.html
    def phone(self):
        if request.method == 'POST':
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
                if not self.valitade.valitdate_phone(phone) or not self.valitade.valitdate_phone(confirm_phone):
                    data = {'msg': 'Digite um telefone válido', "verified": True, "to_update": f'{session.get("to_update")}'}
                    # print(phone, confirm_phone)
                    return template_render("update_data.html", **data)
                
                #adiciona os paranteses
                phone = f"({phone[:2]}){phone[2:]}"
                confirm_phone = f"({confirm_phone[:2]}){confirm_phone[2:]}"

                #verifica se ambos sao iguais
                if not phone == confirm_phone:
                    data = {'msg': 'Os campos devem ser iguais', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
                #atualiza a tabela e devolve pro dashboard
                self.update.exe_update(data={"phone": f"{phone}"}, table_name='user_data', 
                                       data_where={'id': f'{session.get("user_id")}'}, operator='=, =')
                
                #Limpa a session to update
                session.pop('to_update', None)
                data = {'authorize': 'Telefone atualizado com sucesso!', 'redirect_url': '/account/index'}
                return template_render("update_data.html", **data)

            result = self.validate_data()
            

            if not result[0]:
                data = result[1]
                return template_render("update_data.html", **data) 
            #passa oq o usuario vai alterar pela sessao
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
                if not self.valitade.valitdate_email(email, False) or not self.valitade.valitdate_email(confirm_email, False):
                    data = {'msg': 'email invalido', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
            
                #verifica se ambos sao iguais
                if not email == confirm_email:
                    data = {'msg': 'Os campos devem ser iguais', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)

                self.update.exe_update(data={"email": f"{email}"}, table_name='user_data', 
                                       data_where={'id': f'{session.get("user_id")}'}, operator='=, =')
                
                #Limpa a session to update
                session.pop('to_update', None)
                data = {'authorize': 'Email atualizado com sucesso!', 'redirect_url': url_for("main_routes.route_method", route_name="account", method="index")}
                return template_render("update_data.html", **data)

            #1°parte
            result = self.validate_data()
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

                if not self.valitade.valitdate_password(password) or not self.valitade.valitdate_password(confirm_password):
                    data = {'msg': 'senha invalida', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
                if not password == confirm_password:
                    data = {'msg': 'Os campos devem ser iguais', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
                encrypted_password = self.valitade.encryption(password)
                self.update.exe_update(data={"password": f"{encrypted_password}"}, table_name='user_data', 
                                       data_where={'id': f'{session.get("user_id")}'}, operator='=, =')
                
                #Limpa a session to update
                session.pop('to_update', None)
                data = {'authorize': 'Senha atualizada com sucesso!', 'redirect_url': url_for("main_routes.route_method", route_name="account", method="index")}
                return template_render("update_data.html", **data)
        
        #1°parte
            result = self.validate_data()
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
                    data = {'msg': 'Digite um nome valido', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                #verifica se os nomes sao iguais
                if not name.lower() == confirm_name.lower():
                    data = {'msg': 'Os campos devem ser iguais', "verified": True, "to_update": f'{session.get("to_update")}'}

                    return template_render("update_data.html", **data)
                
                #se tudo der certo
                self.update.exe_update(data={"name": f"{name.title()}"}, table_name='user_data', 
                                       data_where={'id': f'{session.get("user_id")}'}, operator='=, =')
                #Limpa a session to update
                session.pop('to_update', None)
                data = {'authorize': 'Nome atualizado com sucesso!', 'redirect_url': url_for("main_routes.route_method", route_name="account", method="index")}
                return template_render("update_data.html", **data)

            result = self.validate_data()
            if not result[0]:
                data = result[1]
                return template_render("update_data.html", **data) 
            #passa oq o usuario vai alterar pela sessao
            session['to_update'] = 'name'  
            return template_render('verify.html') 

        return template_render('update_data.html')