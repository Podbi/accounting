from django.conf.urls import url

from . import views

app_name = 'record'
urlpatterns = [
    url(r'^$', views.IndexView.index, name='index'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.RecordView.edit, name='edit'),
    url(r'^create/$', views.RecordView.create, name='create'),
    url(r'^type/edit/(?P<pk>[0-9]+)/$', views.RecordTypeView.edit, name='type_edit'),
    url(r'^type/create/$', views.RecordTypeView.create, name='type_create'),
    url(r'^month/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.MonthView.month, name='month'),
    url(r'^year/(?P<year>[0-9]{4})$', views.YearView.year, name='year'),
    url(r'^month-summary/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.MonthSummaryView.month, name='month_summary'),
    url(r'^year-summary/(?P<year>[0-9]{4})$', views.YearSummaryView.year, name='year_summary'),
    url(r'^year-by-month-summary/(?P<year>[0-9]{4})$', views.YearSummaryView.byMonth, name='year_by_month_summary'),
    url(r'^type-month/(?P<type>[0-9]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', views.MonthTypeView.type, name='type_month'),
    url(r'^type-year/(?P<type>[0-9]+)/(?P<year>[0-9]{4})$', views.YearTypeView.type, name='type_year'),
    url(r'^types', views.RecordTypeView.list, name='types')
]