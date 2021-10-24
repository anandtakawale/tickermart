from django.shortcuts import render

from pnf.models import Breakout_stock
from .forms import PNFForm
from datetime import datetime, timedelta, date


# Create your views here.
def pnf_home(request):
    if request.method == "POST":
        my_form = PNFForm(request.POST)
        if my_form.is_valid():
            data_date = my_form.cleaned_data["date"]
        else:
            print(my_form.errors)
    else:
        data_date = date.today()
    if data_date == date.today():
        datestr = "today"
    else:
        datestr = data_date.strftime("%d-%m-%Y")
    bostocks = Breakout_stock.objects.filter(date = data_date, breakout = True)
    bdstocks = Breakout_stock.objects.filter(date = data_date, breakout = False)
    prev_date = data_date
    i = 0
    while (not bostocks) and (not bdstocks):
        prev_date = prev_date - timedelta(days = 1)
        bostocks = Breakout_stock.objects.filter(date = prev_date, breakout = True)
        bdstocks = Breakout_stock.objects.filter(date = prev_date, breakout = False)
        i = i + 1
        if i >= 5:
            break
    my_form = PNFForm()
    context = {"form":my_form, "bostocks": bostocks, "bdstocks": bdstocks, "date": datestr }
    return render(request, 'pnf/home.html', context)