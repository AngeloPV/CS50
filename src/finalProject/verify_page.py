from flask import session
import os


class verify_page:
    def __init__(self):
        self.protect_pages = []
        self.public_pages = []
        self.private_pages = []
        
        self.msg = ''
        self.dir = ''

    def get_msg(self):
        return self.msg
    
    def get_dir(self):
        return self.dir

    def pages(self, page):

        self.get_public_pages()
        self.get_private_pages()
        self.get_procted_pages()

        if page in self.public_pages:
            self.dir = "public_pages"

            return True
        elif page in self.private_pages:
            if "user_id" in session:
                self.dir = "private_pages"

                return True
            
            self.msg = 'Voce precisa estar logado'
            return False
        elif page in self.protect_pages:
            self.msg = 'Não é possivel acessar este arquivo'  
            return False

        self.msg = 'Arquivo inexistente'  
        return False
    

    def get_public_pages(self):
        home_path =  os.getcwd()    
        search_dir = 'public_pages'

        dir_found = None
        for root, dirs, files in os.walk(home_path):
            if search_dir in dirs:
                dir_found = os.path.join(root, search_dir)  
                break

        if dir_found:
            files = os.listdir(dir_found)
            
            for file in files:
                file = os.path.splitext(file) 

                if file[0] == "__init__":
                    continue

                self.public_pages.append(file[0])
    
    
    def get_private_pages(self):
        home_path =  os.getcwd()    
        search_dir = 'private_pages'

        dir_found = None
        for root, dirs, files in os.walk(home_path):
            if search_dir in dirs:
                dir_found = os.path.join(root, search_dir)  
                break

        if dir_found:
            files = os.listdir(dir_found)
            
            for file in files:
                file = os.path.splitext(file) 

                if file[0] == "__init__":
                    continue

                self.private_pages.append(file[0])


    def get_procted_pages(self):
        home_path =  os.getcwd()    
        search_dir = 'protected_pages'

        dir_found = None
        for root, dirs, files in os.walk(home_path):
            if search_dir in dirs:
                dir_found = os.path.join(root, search_dir)  
                break
        
        if dir_found:
            files = os.listdir(dir_found)
        
            for file in files:
                file = os.path.splitext(file) 
                
                if file[0] == "__init__":
                    continue   
                
                self.protect_pages.append(file[0])

