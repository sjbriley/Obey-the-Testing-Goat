from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    #If we receiver a post, we redirect
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
        
    items = Item.objects.all()
    return render(request, 'home.html', {
        'items': items
    }) 