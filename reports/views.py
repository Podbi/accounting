from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Record
from .forms import RecordForm
from .service import MonthSummaryCalculator
from .service import DateFactory

class IndexView(generic.ListView):
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
    
class MonthView:
    def month(request, year, month):
        calculator = MonthSummaryCalculator()
        rows = calculator.calculate(
            DateFactory().createFirstDayOfMonth(int(month), int(year)),
            DateFactory().createLastDayOfMonth(int(month), int(year))
        )
        return render(request, 'reports/month.html', {'month' : month, 'year' : year, 'rows' : rows})