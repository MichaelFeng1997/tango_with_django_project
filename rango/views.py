from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    #construct a dictionary to pass to the template engine as its context
    # Note the key boldmessage is the same as {{boldmessage}} in the template
    context_dict = {'boldmessage': "chunchy,creamy,cookie,candy,cupcake!"}
    return render(request, 'rango/index.html',context = context_dict)

def about(request):
    context_dict2 = {'boldmessage': "hey!"}
    return render(request, 'rango/about.html',context = context_dict2)