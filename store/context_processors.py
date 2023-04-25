from .models import Category
from payment.models import *
from django.shortcuts import redirect
def categories(request):
    return{
        'usa': Category.objects.filter(location=0),   
        'germany': Category.objects.filter(location=1),  
        'australia': Category.objects.filter(location=2),  
        'pua': Category.objects.filter(location=3),
        'canada': Category.objects.filter(location=4),
        'credit': Category.objects.filter(location=5),
        'categories': Category.objects.filter(location=-1),
        'category': Category.objects.all()
    }

def balance(request):
    if request.user.is_authenticated:
        balance = Balance.objects.filter(created_by=request.user).first()
        if balance and balance.balance is not None:
            b = round(balance.balance, 2)
            return {'balance': b}
        else:
            b = 0.00
            return {'balance': b}
    else:
        b = 0.00
        return {'balance': b}
    
def invoice(request):
    if request.user.is_authenticated:
        invoice = Invoice.objects.filter(created_by=request.user,sold=True).first()
        return {'invoice':invoice}
    else:
        invoice = 0
        return {'invoice':invoice}

import random
from django.http import JsonResponse
import random
import time

import time
import random

def random_name(request):
    names = ['John', 'Jane', 'Mike', 'Sarah', 'David']
    bank_names = ['Bank of America', 'Chase', 'Wells Fargo', 'Citibank', 'US Bank']
    name1 = random.choice(names)
    bank_name1 = random.choice(bank_names)
    name2 = random.choice(names)
    bank_name2 = random.choice(bank_names)
    name3 = random.choice(names)
    bank_name3 = random.choice(bank_names)
    name4 = random.choice(names)
    bank_name4 = random.choice(bank_names)
    name5 = random.choice(names)
    bank_name5 = random.choice(bank_names)
    data = {
        'human_name': name1,
        'bank_name': bank_name1,
        'human_name1': name2,
        'bank_name1': bank_name2,
        'human_name2': name3,
        'bank_name2': bank_name3,
        'human_name3': name4,
        'bank_name3': bank_name4,
        'human_name4': name5,
        'bank_name4': bank_name5,
        
    }
    
    return data