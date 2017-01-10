from reports.services.monthSummaryCalculator import MonthSummaryCalculator
from reports.services.yearSummaryCalculator import YearSummaryCalculator
from reports.services.balanceCalculator import BalanceCalculator

def menu_context_processor(request):
    return {
        'monthSummaries' : MonthSummaryCalculator().listOfAvailable(), 
        'yearSummaries' : YearSummaryCalculator().listOfAvailable()
    }

def balance_context_processor(request):
    return {
        'balance' : BalanceCalculator().calculate()
    }
