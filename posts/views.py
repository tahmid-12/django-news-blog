from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect

from .forms import NewItemForm, EditItemForm

from .models import Item
from django.contrib.auth import get_user_model

# Create your views here.
def detail(request, pk):
    # item = get_list_or_404(Item, pk=pk)
    item = Item.objects.get(pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)[0:3]
    return render(request, 'details.html',{
        'item': item,
        'related_items': related_items
    })

def writer(request,pk):
    User = get_user_model()
    item = Item.objects.filter(pk=pk).values('created_by_id')
    print("item",item)
    instance = User.objects.values_list('id')
    # instance = User.objects.get(id=item)
    # instance = User.objects.filter(id=item)
    print("Author ID",instance)
    # author = User.objects.filter('id')
    # print("Author",author)
    return render(request, 'profile.html',{
        'item': item
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('posts:detail', pk=item.id)
    
    else:
        form = NewItemForm()

    return render(request,'form.html',{
        'form': form,
        'title': 'New News'
    })

@login_required
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('posts:detail', pk=item.id)
    
    else:
        form = EditItemForm(instance=item)

    return render(request,'form.html',{
        'form': form,
        'title': 'Edit News'
    })



@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')


