from django.conf.urls import url
from . import views

app_name = 'groceries'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'lend/(?P<lend_id>[0-9]+)/$', views.lenditem, name='lend'),
    url(r'hist/(?P<lend_id>[0-9]+)/$', views.itemhist, name='hist'),
]
