from django_currentuser.middleware import get_current_authenticated_user
from chat.models import UserTracking

def update_user_tracking(msg):
     user = get_current_authenticated_user()
     if user:
        try:
            ut_obj = UserTracking.objects.get(user=user, button_type=msg)
            ut_obj.count = ut_obj.count+1
            ut_obj.save()
        except Exception as e:
            ut_obj = UserTracking()
            ut_obj.user = user
            ut_obj.button_type= msg
            ut_obj.count = 1
            ut_obj.save()     

         



