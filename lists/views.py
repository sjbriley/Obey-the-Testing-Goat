from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()}) 

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list':list_, 'form': form})
    """
        try:
            item = Item(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"
            
    form = ItemForm()    
    return render(request, 'list.html', {
        'list': list_,
        'error': error,
        'form': form
    })
    """

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form':form})
    """
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    #return redirect('view_list', list_.id)
    return redirect(list_) # get_absolute_url() in models.py automatically redirects
    """