import json
import requests
import random

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from chat.forms import SignUpForm
from chat.models import UserTracking
from chat.utils import update_user_tracking



def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)


def respond_to_websockets(message):
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
     }  

    result_message = {
        'type': 'text'
    }

    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])
        update_user_tracking(UserTracking.FAT)
    
    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
        update_user_tracking(UserTracking.STUPID)
    
    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])
        update_user_tracking(UserTracking.DUMB)

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message

class UserRegistrationView(generic.FormView):
    form_class = SignUpForm
    success_url = "/chat/"	
    template_name = "chatbot_tutorial/register.html"

    def form_valid(self, form):
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(self.request, user)
            return redirect('chat')

class UserTrackingListViewJSON(BaseDatatableView):
    model = UserTracking
    columns = ['id', 'user', 'button_type', 'count']
    order_columns = ['id', 'user', 'button_type', 'count']
    max_display_length = 500

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'button_type':
            return '{0}'.format(row.get_button_type_display())
        elif column == 'user':
            return '{0}'.format(row.user.get_full_name() if row.user.get_full_name() else row.user.username )    
        else:
            return super(UserTrackingListViewJSON, self).render_column(row, column)

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            qs = qs.filter(Q(user__username__istartswith=sSearch) | Q(user__first_name__istartswith=sSearch) | Q(user__last_name__istartswith=sSearch))
        return qs


class UserTrackingView(generic.TemplateView):
    template_name = "chatbot_tutorial/user_tacking_listing.html"               	    