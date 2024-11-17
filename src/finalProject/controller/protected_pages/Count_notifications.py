from ...helper.helper_select import Select
from flask import session

class Count_notifications():
    def __init__(self):
        self.select = Select()
        
    def get_count(self): 
        self.select.exe_select('''SELECT COUNT(id) FROM user_notification WHERE sit_notification = %s AND user_id = %s LIMIT %s''',
                            f'{{"sit_notifcation": "1", "user_id": "{session["user_id"]}", "LIMIT": "1"}}', True)
        
        if self.select.get_result():
            return self.select.get_result()[0]
        
        return 0
