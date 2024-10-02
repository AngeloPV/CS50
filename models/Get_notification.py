from ..helper.helper_select import Select
from ..helper.helper_delete import Delete
from ..helper.helper_update import Update

from flask import session

class Get_notifications():
    def __init__(self):
        self.select = Select()
        self.update = Update()
        self.delete_notification = Delete()

    def select_notifcation(self, type):
        print(type)
        self.select.exe_select('''SELECT NT.type, NT.content, NT.subject, NT.created, UN.id, UN.sit_notfication FROM notification AS NT
                               LEFT JOIN user_notification AS UN ON NT.id = UN.notification_id WHERE UN.user_id = %s AND UN.type = %s''', 
                               f'{{"user_id": "52", "type": "{type}"}}', True)
        
        if self.select.get_result():
            return self.select.get_result()
        
        return False
    
        
    def delete_notifications(self, data):
        if isinstance(data, list):
            placeholder = ','.join(['%s'] * len(data))
            self.delete_notification.exe_delete("user_notification", data, f'id IN ({placeholder})', True)
        elif isinstance(data, int):
            self.delete_notification.exe_delete("user_notification", data, f'id = %s', True)

        if self.delete_notification.getResult():
            return True
        
        return False
    
    def update_notifications(self, value_update, values_id):

        if isinstance(value_update, int):
            data = {"sit_notfication": value_update}   
        else:
            data = {"type": value_update}   

        data_where = {"user_id": "52", 'id': values_id}
        
        if isinstance(values_id, list):
            for i in range(len(values_id)):
                values_id[i] = int(values_id[i])
            
            # print(list_id)
            self.update.exe_update(data=data, table_name="user_notification", data_where=data_where, operator=' =, =, IN', close_conn=True)
        elif isinstance(values_id, int):
            self.update.exe_update(data=data, table_name="user_notification", data_where=data_where, operator=' =, =, =', close_conn=True)

        if self.update.getResult():
            return True
        
        return False