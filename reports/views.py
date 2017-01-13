from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Record
from .models import RecordType
from .forms import RecordForm
from .forms import RecordTypeForm
from reports.services.monthSummaryCalculator import MonthSummaryCalculator
from reports.services.monthTranslator import MonthTranslator
from reports.services.dateFactory import DateFactory
from reports.services.recordTypeRepository import RecordTypeRepository
from reports.services.recordSummaryRepository import RecordSummaryRepository

class IndexView:
    def index(request):
        records = Record.objects.order_by('-date')
        paginator = Paginator(records, 20)
        
        page = request.GET.get('page')
        try:
            records = paginator.page(page)
        except PageNotAnInteger:
            records = paginator.page(1)
        except EmptyPage:
            records = paginator.page(paginator.num_pages)
            
        return render(request, 'reports/index.html', {'records' : records})

class RecordView:
    def edit(request, pk):
        record = get_object_or_404(Record, pk=pk)
        if request.method == 'POST':
            form = RecordForm(request.POST, instance=record)
            if form.is_valid():
                record = form.save()
                return redirect('record:index')
        else:
            form = RecordForm(instance=record)    
    
        return render(request, 'reports/record.html', {'form' : form})
    
    def create(request):
        if request.method == 'POST':
            form = RecordForm(request.POST)
            if form.is_valid():
                record = form.save()
                return redirect('record:index')
        else:
            form = RecordForm()
        return render(request, 'reports/new.html', {'form' : form})
    
class MonthSummaryView:
    def month(request, year, month):
        calculator = MonthSummaryCalculator()
        summary = calculator.calculate(
            DateFactory().createFirstDayOfMonth(int(month), int(year)),
            DateFactory().createLastDayOfMonth(int(month), int(year)),
            'CZK'
        )
        
        month = int(month)
        year = int(year)
        
        return render(request, 'reports/month_summary.html', {
            'month' : MonthTranslator().translate(month), 
            'monthId' : "%02d" % month,
            'year' : "%04d" % year, 
            'summary' : summary,
            'previous' : reverse('record:month_summary', kwargs={
                'month': "%02d" % (12 if month == 1 else month - 1), 
                'year' : year - 1 if month == 1 else year
            }),
            'next' : reverse('record:month_summary', kwargs={
                'month': "%02d" % (1 if month == 12 else month + 1), 
                'year' : year + 1 if month == 12 else year
            })
        })
        
class YearSummaryView:
    def year(request, year):
        calculator = MonthSummaryCalculator()
        summary = calculator.calculate(
            DateFactory().createFirstDayOfMonth(1, int(year)),
            DateFactory().createLastDayOfMonth(12, int(year)),
            'CZK'
        )
        
        year = int(year)
        
        return render(request, 'reports/year_summary.html', {
            'year' : "%04d" % year, 
            'summary' : summary,
            'previous' : reverse('record:year_summary', kwargs={
                'year' : year - 1
            }),
            'next' : reverse('record:year_summary', kwargs={
                'year' : year + 1
            })
        })
    
class MonthView:
    def month(request, year, month):
        records = RecordSummaryRepository().findAllByDates(
            DateFactory().createFirstDayOfMonth(int(month), int(year)),
            DateFactory().createLastDayOfMonth(int(month), int(year)),
            'CZK'
        )
        
        summary = 0.00;
        for record in records:
            summary += record.money
        
        return render(request, 'reports/month.html', {
            'month' : MonthTranslator().translate(int(month)), 
            'monthId': month,
            'year' : year, 
            'records' : records,
            'summary' : summary,
            'currency' : 'CZK'
        })

class MonthTypeView:
    def type(request, year, month, type):
        type = get_object_or_404(RecordType, pk=type)
        records = RecordTypeRepository().findAllByTypeAndDates(
            type.id,
            DateFactory().createFirstDayOfMonth(int(month), int(year)),
            DateFactory().createLastDayOfMonth(int(month), int(year)),
            'CZK'
        )
        
        summary = 0.00;
        for record in records:
            summary += record.money
        
        return render(request, 'reports/type_month.html', {
            'month' : MonthTranslator().translate(int(month)), 
            'monthId': month,
            'type' : type,
            'year' : year, 
            'records' : records,
            'summary' : summary,
            'currency' : 'CZK'
        })
        
class YearView:
    def year(request, year):
        records = RecordSummaryRepository().findAllByDates(
            DateFactory().createFirstDayOfMonth(1, int(year)),
            DateFactory().createLastDayOfMonth(12, int(year)),
            'CZK'
        )
        
        summary = 0.00;
        for record in records:
            summary += record.money
        
        return render(request, 'reports/year.html', {
            'year' : year, 
            'records' : records,
            'summary' : summary,
            'currency' : 'CZK'
        })

class YearTypeView:
    def type(request, year, type):
        type = get_object_or_404(RecordType, pk=type)
        records = RecordTypeRepository().findAllByTypeAndDates(
            type.id,
            DateFactory().createFirstDayOfMonth(1, int(year)),
            DateFactory().createLastDayOfMonth(12, int(year)),
            'CZK'
        )
        
        summary = 0.00;
        for record in records:
            summary += record.money
        
        return render(request, 'reports/type_year.html', {
            'type' : type,
            'year' : year, 
            'records' : records,
            'summary' : summary,
            'currency' : 'CZK'
        })
        
class RecordTypeView:
    def list(request):
        types = RecordTypeRepository().findAllWithCount()
        
        return render(request, 'reports/types.html', {
            'types' : types
        })

    def edit(request, pk):
        type = get_object_or_404(RecordType, pk=pk)
        if request.method == 'POST':
            form = RecordTypeForm(request.POST, instance=type)
            if form.is_valid():
                record = form.save()
                return redirect('record:types')
        else:
            form = RecordTypeForm(instance=type)    
    
        return render(request, 'reports/type.html', {'form' : form})
    
    def create(request):
        if request.method == 'POST':
            form = RecordTypeForm(request.POST)
            if form.is_valid():
                record = form.save()
                return redirect('record:types')
        else:
            form = RecordTypeForm()
        return render(request, 'reports/type.html', {'form' : form})
        
        