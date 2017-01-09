from reports.services.monthSummaryCalculator import MonthSummaryCalculator
from reports.services.yearSummaryCalculator import YearSummaryCalculator

def menu_processor(request):
    return {
        'monthSummaries' : MonthSummaryCalculator().listOfAvailable(), 
        'yearSummaries' : YearSummaryCalculator().listOfAvailable()
    }