from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Record
from .models import RecordType
from .forms import RecordForm
from .service import MonthSummaryCalculator
from .service import MonthTranslator
from .service import DateFactory
from .service import RecordTypeRepository
from .service import RecordByMonthRepository

class IndexView(generic.ListView):
    template_name = 'reports/index.html'
    context_object_name = 'all_records_list'
    
    def get_queryset(self):
        return Record.objects.order_by('-date')[:20]

class RecordListView(generic.ListView):
    template_name = 'reports/index.html'
    context_object_name = 'all_records_list'
    
    def get_queryset(self):
        return Record.objects.order_by('-date')

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
        