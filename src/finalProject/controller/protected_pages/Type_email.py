import re
from flask import session 
from ...app import app
from ...config import Config


class Type_email:
    def __init__(self): 
        self.email_config = Config() 
        self.result = None 
        self.current_provider = 'gmail'  # Store current provider

    def get_result_email(self):
        return self.result
    
    def get_type(self, email):
        match = re.search(r'@(.+?)\.', email)

        if match:
            provider = match.group(1)  # Gets the found content
            
            if provider != self.current_provider:  # Checks if the provider has changed
                self.current_provider = provider  
                with app.app_context():
                    self.email_config.get_set_email(app, self.current_provider)  # Update settings

            self.result = provider
            return True

        return None
