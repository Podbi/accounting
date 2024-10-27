from django.forms import ModelForm

from .models import Record
from .models import RecordType

class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['date', 'description', 'place', 'type', 'money', 'currency', 'source', 'category']

class RecordTypeForm(ModelForm):
    class Meta:
        model = RecordType
        fields = ['name']
    