import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import Permission
from .models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import redirect, render
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
    user = create_or_update_user_info(access_token)
    login(request, user)
    return redirect(reverse('admin:index'))
  raise Http404


def create_or_update_user_info(access_token):
  endpoint = settings.ONEAUTH_USER_INFO_URL
  headers = {
    "Authorization": "Bearer {}".format(access_token)
  }
  response = requests.get(endpoint, headers=headers)
  user_data_json = response.json()
  defaults = {
    'oneauth_id': user_data_json.get('id'),
    'username': user_data_json.get('username'),
    'email': user_data_json.get('verifiedemail') if user_data_json.get('verifiedemail') else user_data_json.get('email'),
    'first_name': user_data_json.get('firstname'),
    'last_name': user_data_json.get('lastname'),
  }

  user, created = User.objects.update_or_create(oneauth_id=defaults['oneauth_id'], defaults=defaults)
  if created:
    # change user permission and staff status only when user is created
    user.is_staff = True
    permissions = Permission.objects.filter(
      Q(codename__istartswith='add') | Q(codename__istartswith='view'),
      content_type__app_label='cron'
    )
    user.user_permissions.set(permissions)
    user.save()
  return user


def login_view(request):
  if request.user.is_authenticated:
    return redirect(reverse('admin:index'))

  context = {
    'oneauth_authorization_url': "https://account.codingblocks.com/oauth/authorize?response_type=code&client_id={}&redirect_uri={}".format(
      settings.ONEAUTH_CLIENT_ID, request.build_absolute_uri(reverse('oneauth_callback_url')))
  }
  return render(request, 'login.html', context=context)
