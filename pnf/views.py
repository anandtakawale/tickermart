from django.shortcuts import redirect, render

from pnf.models import Breakout_stock
from .forms import PNFForm
from datetime import datetime
from django.urls import reverse

# Create your views here.
def pnf_home(request):
    if request.method == "POST":
        my_form = PNFForm(request.POST)
        if my_form.is_valid():
            datestr = my_form.cleaned_data["date"].strftime("%d-%m-%Y")
            return redirect(reverse("bostocks", kwargs={"datestr":datestr}))
        else:
            print(my_form.errors)
        
    else:
        my_form = PNFForm()
        context = {
            'form':my_form,
        }
        return render(request, 'pnf/home.html', context)

def pnf_date(request, datestr):
    date = datetime.strptime(datestr, '%d-%m-%Y').date()
    bostocks = Breakout_stock.objects.filter(date = date, breakout = True)
    bdstocks = Breakout_stock.objects.filter(date = date, breakout = False)
    context = { "bostocks": bostocks, "bdstocks": bdstocks, "date": datestr }
    return render(request, 'pnf/bostocks.html', context)