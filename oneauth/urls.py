from django.urls import path

from oneauth import views

urlpatterns = [
    path('callback/', views.callback_view, name='oneauth_callback_url'),
    path('login/', views.login_view, name='login')
]
