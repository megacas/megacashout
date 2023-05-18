from django.shortcuts import render, get_object_or_404
from .models import *
from payment.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from .context_processors import random_name
@login_required
def home(request):
    return render(request,"home.html",)

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})

def trial(request):
    
    return JsonResponse(random_name(request))

from django.http import FileResponse
import os

def download_csv(request):
    file_path = '/static/output.csv'  # Replace with the actual path to the exported CSV file

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = FileResponse(file)
            response['Content-Type'] = 'text/csv'
            response['Content-Disposition'] = 'attachment; filename="output.csv"'
            return response
    else:
        return HttpResponse('File not found.')
