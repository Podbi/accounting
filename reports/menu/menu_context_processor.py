from ..service import MonthSummaryCalculator

def menu_processor(request):
    return {'monthSummaries' : MonthSummaryCalculator().listOfAvailable()}