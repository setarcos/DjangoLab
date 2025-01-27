from django.urls import path
from . import views

app_name = 'linux'
urlpatterns = [
    path('', views.index, name='index'),
    path('pubkey', views.pubkey, name='pubkey'),
    path('gituser', views.gituser, name='gituser'),
    path('resetuser', views.resetUser, name='resetUser'),
]
