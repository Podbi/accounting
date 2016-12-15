from django.conf.urls import url

from . import views

app_name = 'record'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.RecordView.edit, name='edit'),
    url(r'^create/$', views.RecordView.create, name='create')
]