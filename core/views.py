from django.shortcuts import render,redirect
from posts.models import Category, Item
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm

# Create your views here.
def index(request):
    items = Item.objects.all();
    categories = Category.objects.all();

    return render(request,'pages\index.html',{
        'categories': categories,
        'items': items, 
    })

def contact(request):
    return render(request,'pages\contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request,'pages/signup.html',{
        'form': form
    })

@login_required
def logout(request):
    logout(request)
    return redirect('/')
 