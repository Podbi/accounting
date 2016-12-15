from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Record
from .forms import RecordForm

class IndexView(generic.ListView):
    template_name = 'reports/index.html'
    context_object_name = 'latest_record_list'
    
    def get_queryset(self):
        return Record.objects.order_by('-date')[:5]

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