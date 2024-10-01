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
