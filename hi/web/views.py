from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Product

# Create your views here.
from django.shortcuts import render
#from .models import Candidate, Poll, Choice

# Create your views here.
def index(request):
    return render(request, 'web/one.html')  # html에게 넘겨준다.

def search(request):
    if request.method == 'POST':
        sea = request.POST.get('sea')
        try:
            product = Product.objects.filter(name=sea)
            context = {'product': product[0]}
            return render(request, 'web/two.html', context)
        except:
            return render(request, 'web/no.html')
