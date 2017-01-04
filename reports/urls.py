from django.conf.urls import url

from . import views

app_name = 'record'
urlpatterns = [
    url(r'^$', views.IndexView.index, name='index'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.RecordView.edit, name='edit'),
    url(r'^create/$', views.RecordView.create, name='create'),
    url(r'^month/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.MonthView.month, name='month'),
    url(r'^month-summary/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.MonthSummaryView.month, name='month_summary'),
    url(r'^type/(?P<type>[0-9]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.MonthTypeView.type, name='type')
]