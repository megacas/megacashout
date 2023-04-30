from django.shortcuts import render, get_object_or_404
from .models import *
from payment.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .context_processors import random_name
@login_required
def home(request):
    return render(request,"home.html",)

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    cards = Category.objects.get(name="Cards")
    return render(request, 'category.html', {'category': category, 'products': products,'cards':cards})

def trial(request):
    
    return JsonResponse(random_name(request))
