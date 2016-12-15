from django.db import models

class MoneySource(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Currency(models.Model):
    code = models.CharField(max_length=3)
    def __str__(self):
        return self.code

class RecordType(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Record(models.Model):
    date = models.DateTimeField()
    description = models.CharField(max_length=255)
    place = models.CharField(max_length=255, null=True)
    type = models.ForeignKey(RecordType, on_delete=models.PROTECT)
    money = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    source = models.ForeignKey(MoneySource, on_delete=models.PROTECT)
    def __str__(self):
        string = self.date.strftime('%d.%m.%Y') if self.date is not None else '' 
        string += ' - ' 
        string += self.description if self.description is not None else ''
        string += ' za ' 
        string += str(self.money) if self.money is not None else ''
        string += ' '
        string += self.currency.code if self.currency is not None else ''
        return string
