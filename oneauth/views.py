import json

import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import redirect
from django.urls import reverse


def callback_view(request):
    if 'code' in request.GET:
        grant_code = request.GET.get('code')
        data = {
            "client_id": settings.ONEAUTH_CLIENT_ID,
            "redirect_uri": request.build_absolute_uri(reverse('oneauth_callback_url')),
            "client_secret": settings.ONEAUTH_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": grant_code
        }
        # exchange access token for grant code
        response = requests.post(settings.ONEAUTH_TOKEN_URL, data=data)
        if response.status_code != 200:
            return HttpResponseForbidden()
        access_token = response.json()['access_token']
        user_info = get_user_info(access_token)
        return HttpResponse(content=json.dumps(user_info), content_type='application/json')
    raise Http404


def get_user_info(access_token):
    endpoint = settings.ONEAUTH_USER_INFO_URL
    headers = {
        "Authorization": "Bearer {}".format(access_token)
    }
    response = requests.get(endpoint, headers=headers)
    user_data_json = response.json()
    return user_data_json


def login_view(request):
    oneauth_authorization_url = "https://account.codingblocks.com/oauth/authorize?response_type=code&client_id={}&redirect_uri={}".format(
        settings.ONEAUTH_CLIENT_ID, request.build_absolute_uri(reverse('oneauth_callback_url')))
    return redirect(oneauth_authorization_url)
