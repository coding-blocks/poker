from django.shortcuts import render, redirect
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from decouple import config
from django.conf import settings
# ONEAUTH_CLIENT_ID = config('ONEAUTH_CLIENT_ID', default='')
# ONEAUTH_CLIENT_SECRET = config('ONEAUTH_CLIENT_SECRET', default='')

# Create your views here.
def callback(request):
    code = request.GET.get('code', '')
    data = {
        "client_id" : settings.ONEAUTH_CLIENT_ID,
        "redirect_uri" : "http://localhost:8000/callback",
        "client_secret" : settings.ONEAUTH_CLIENT_SECRET,
        "grant_type" : "authorization_code",
        "code"  : code
    }
    response = requests.post(f'https://account.codingblocks.com/oauth/token', data=data)
    token = response.json().get('access_token', '')
    response= requests.get('https://account.codingblocks.com/api/users/me', headers={'Authorization': f'Bearer {token}'})
    data = response.json()
    print(data)
    user, _ = User.objects.get_or_create(
                email=data['email'])
    user.username = data.get('username', '')
    user.email = data.get('email', '')
    user.first_name = data.get('firstname', '')
    user.last_name = data.get('lastname', '')
    user.save()
    auth_login(request, user)

    # return redirect(f'https://account.codingblocks.com/oauth/token?client_id=7306329124&client_secret=n0AOB0vHH6rRvqRDIsZTkqSSvmfLklOHZSHd63IiQHvIOarEMPBaYbWx2izjsQil&grant_type=authorization_code&code={code}&redirect_uri=http://localhost:8000/auth')
    return redirect('home')


def login(request):
    return redirect(settings.LOGIN_URL)