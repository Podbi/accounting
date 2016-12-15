from django.contrib import admin

from .models import MoneySource
from .models import Currency
from .models import RecordType
from .models import Record

admin.site.register(MoneySource)
admin.site.register(Currency)
admin.site.register(RecordType)
admin.site.register(Record)