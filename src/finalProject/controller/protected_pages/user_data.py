from ...models.User import User

class User_data:
    def __init__(self):
        self.user_data = User()

    #pega a senha de 4 digitos
    def get_4_digits_pass(self, user_id):
        return self.user_data.get_4_digits_pass(user_id=user_id)

    #define a senha de 4 digitos
    def set_4_digits_pass(self, password, user_id):
        return self.user_data.set_4_digits_pass(password=password, user_id=user_id)
    
    #pega a foto de perfil
    def get_profile_img(self, user_id):        
        return self.user_data.get_profile_image(user_id=user_id)
    #define a foto de perfil
    def set_profile_img(self, img, user_id):
        return self.user_data.set_profile_image(img=img, user_id=user_id)

    #retorna uma lista com o nome/sobrenome do usuario separado por virgula, usar o indice pra pegar o 
    #nome desejado, no caso, primeiro e ultimo, chamar indice 0 e indice -1
    def get_user_name(self, user_id):
        return self.user_data.get_user_name(user_id=user_id)
    
    def get_user_email(self, user_id):
        return self.user_data.get_user_email(user_id=user_id)
    
    def get_user_phone(self, user_id):
        return self.user_data.get_user_phone(user_id=user_id)
    
    def get_theme(self, user_id):
        return self.user_data.get_theme(user_id=user_id)
    
    def set_theme(self, user_id, theme):
        return self.user_data.set_theme(user_id=user_id, theme=theme)
    
    def get_language(self, user_id):
        return self.user_data.get_language(user_id=user_id)
    
    def delete_account(self, user_id):
        return self.user_data.delete_account(user_id=user_id)