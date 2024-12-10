from flask import session
from .controller.protected_pages.Count_notifications import Count_notifications

def notifications_processor():
    # a session view_count, irá ficar sendo usada para verificar se a pagina de notifcations ja foi acessado, caso tenha sido ent todas as notifacations pedentes ja foram vistas
    count_notif = 0  # Default value if not authenticated   or not authenticated
    if 'viewd_count' in session and session['viewd_count'] == True:
        return dict(count_notifications=count_notif)  # Returns as dictionary
    
    if "user_id" in session and session.get('viewd_count') == False:
        count_notif = Count_notifications().get_count()  
    return dict(count_notifications=count_notif)  # Returns as dictionary
