from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Record
from .models import RecordType
from .forms import RecordForm
from reports.services.monthSummaryCalculator import MonthSummaryCalculator
from reports.services.monthTranslator import MonthTranslator
from reports.services.dateFactory import DateFactory
from reports.services.recordTypeRepository import RecordTypeRepository
from reports.services.recordByMonthRepository import RecordByMonthRepository

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
        
        return render(request, 'reports/month_summary.html', {
            'month' : MonthTranslator().translate(int(month)), 
            'monthId' : month,
            'year' : year, 
            'summary' : summary
        })
        
class MonthView:
    def month(request, year, month):
        records = RecordByMonthRepository().findAllByDates(
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
        
        return render(request, 'reports/type.html', {
            'month' : MonthTranslator().translate(int(month)), 
            'monthId': month,
            'type' : type,
            'year' : year, 
            'records' : records,
            'summary' : summary,
            'currency' : 'CZK'
        })
        