from ..helper.helper_select import Select
from ..helper.helper_delete import Delete
from ..helper.helper_update import Update

from flask import session
from datetime import datetime

class Get_notifications():
    def __init__(self):
        self.select = Select()
        self.update = Update()
        self.delete_notification = Delete()
        self.result = None


    def select_notifcation(self, type):
        self.select.exe_select('''SELECT NT.type, NT.content, NT.subject, NT.created, UN.id, UN.sit_notification, UN.created FROM notification AS NT
                               LEFT JOIN user_notification AS UN ON NT.id = UN.notification_id WHERE UN.user_id = %s AND UN.type = %s 
                               ORDER BY CASE WHEN UN.changed = 1 THEN UN.created ELSE COALESCE(UN.modified, UN.created) END DESC;''', 
                               f'{{"user_id": "{session["user_id"]}", "type": "{type}"}}', False)
    

        self.result = self.select.get_result()

        if self.result:
            self.result = list(self.select.get_result())

            self.datetime_notifcations()

            return self.result, self.count_notifications()

        return False, self.count_notifications()


    def count_notifications(self):
        self.select.exe_select('''SELECT COUNT(id) FROM user_notification WHERE user_id = %s''', f'{{"user_id": "{session["user_id"]}" }}', False)
        all_notifcations = self.select.get_result()[0][0]

        types = {'standard': 0, 'archive': 0, 'favorite': 0}

        for type in types:
            if type == 'favorite':
                self.select.exe_select('''SELECT COUNT(id) FROM user_notification WHERE user_id = %s AND type = %s''', 
                                       f'{{"user_id": "{session["user_id"]}", "type": "{type}"}}', True)
                
                types[type] = self.select.get_result()[0][0]
                break

            self.select.exe_select('''SELECT COUNT(id) FROM user_notification WHERE user_id = %s AND type = %s''', 
                                   f'{{"user_id": "{session["user_id"]}", "type": "{type}"}}', False)
            

            types[type] = self.select.get_result()[0][0]

        types['all'] = all_notifcations

        return types


    def datetime_notifcations(self):
        now = datetime.now()

        for i, v in enumerate(self.result):
            self.result[i] = list(self.result[i])
            if self.result[i][6].strftime('%Y') != now.strftime('%Y'):
                self.result[i][6] = self.result[i][6].strftime("%Y %b")
                continue
            elif self.result[i][6].strftime('%m') != now.strftime('%m') or self.result[i][6].strftime('%d') != now.strftime('%d'):
                self.result[i][6] = self.result[i][6].strftime("%b %d")
                continue
            elif self.result[i][6].strftime('%H') != now.strftime('%H'):
                self.result[i][6] = self.result[i][6].strftime("%I:%M %p")
                continue
            elif self.result[i][6].strftime('%M') != now.strftime('%M'):
                difference_time = now - self.result[i][6] 

                difference_min = difference_time.total_seconds() // 60  

                if (difference_min <= 3.0):
                    self.result[i][6] = f'Just now'
                    continue
                self.result[i][6] = f'{int(difference_min)} min ago'
            else:
                self.result[i][6] = f'Just now'


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
        print(value_update)
        if value_update == 0:
            return True
        if isinstance(value_update, int):
            print(value_update)
            data = {"sit_notification": value_update}   
        else:
            data = {"type": value_update, "changed": 0}       

        data_where = {"user_id": session['user_id'], 'id': values_id}
        

        operator_map = {
            (int, list): ' =, =, IN',
            (int, int): ' =, =, =',
            (str, list): ' =, =, =, IN',  # Assume que `value_update` não é int
        }

        key_map = (type(value_update), type(values_id))

        if isinstance(values_id, list):

            for i in range(len(data_where['id'])):
                data_where['id'][i] = int(data_where['id'][i])
    
            self.update.exe_update(data=data, table_name="user_notification", data_where=data_where, operator=operator_map.get(key_map, ' =, =, =, ='), close_conn=True)
        elif isinstance(values_id, int): 
            self.update.exe_update(data=data, table_name="user_notification", data_where=data_where, operator=operator_map.get(key_map, ' =, =, =, ='), close_conn=True)

        if self.update.getResult():
            return True
        
        return False
