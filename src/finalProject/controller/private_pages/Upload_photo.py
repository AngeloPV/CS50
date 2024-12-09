from flask import request, session, redirect, url_for
from ...renderer import template_render
from werkzeug.utils import secure_filename
from PIL import Image  # Pillow para manipulação de imagens
from ...models.User import User
import os


class Upload_photo:
    """
    Classe responsavel por mudar a foto de perfil do usuario
    """
    def __init__(self):
        self.user = User() #cria uma instancia da classe responsavel por pegar os dados do usuario

    def index(self):
        """
        Renderiza um form onde o usuário poderá escolher uma foto em seu computador, enviar para o form
        e se a extensão da foto for compatível, ela será salvo na pasta static/images/users e o nome
        do arquivo será salvo no banco de dados
        """
        if request.method == 'POST':
            # Pega o envio do arquivo
            file = request.files['profilePic']
            
            if file:
                filename = secure_filename(file.filename)
                file_extension = os.path.splitext(filename)[1]  # pega a extensão do arquivo (ex: .jpg, .png)

                # apenas será aceito imagens nos formatos suportados
                if file_extension.lower() not in ['.png', '.jpg', '.jpeg', '.webp']:
                    data = {"msg": "Invalid image format. Only .jpg, .jpeg, .webp and .png are supported."}
                    return template_render('upload_photo.html', **data)

                # define o nome do novo arquivo
                new_filename = f'profile_image_user_{session.get("user_id")}{file_extension}'

                #salva a imagem em static/images/users
                current_dir = os.path.dirname(__file__)
                save_dir = os.path.join(current_dir, '..', '..', 'static', 'images', 'users')
                os.makedirs(save_dir, exist_ok=True)
                file_path = os.path.join(save_dir, new_filename)

                # Abre a imagem usando PIL
                image = Image.open(file)

                #verifica o tamanho da imagem
                width, height = image.size
                if width < 150 or height < 150:
                    data = {"msg": "Image too small. The minimum size is 150x150 pixels."}
                    return template_render('upload_photo.html', **data)

                if width > 1280 or height > 720:
                    data = {"msg": "Image too large. The maximum size is 1280x720 pixels."}
                    return template_render('upload_photo.html', **data)


                image.thumbnail((500, 500))

                image.save(file_path)  

                # Salva o nome da imagem no banco de dados
                self.user.set_profile_image(img=new_filename, user_id=session.get("user_id"))

                return redirect(url_for("main_routes.route_method", route_name="dashboard", method="index"))

            #retorna erro caso nao seja selecionado nenhum arquivo
            data = {"msg": "Upload a photo"}
            return template_render('upload_photo.html', **data)

        return template_render('upload_photo.html')
