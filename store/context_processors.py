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
    names = ['Kolaskov','Mclean', 'Trevor', 'Rexxy', 'Sarah', 'David', 'Draven', 'Raven', 'Malachi', 'Lilith', 'Azazel', 'Morgana', 'Damien', 'Bellatrix', 'Lucius', 'Luna', 'Salem', 'Morticia', 'Vladimir', 'Selene', 'Spike','Devon']
    bank_names = ['Bank of America', 'Chase', 'Wells Fargo', 'Citibank', 'US Bank', 'HSBC', 'Barclays', 'TD Bank', 'PNC Bank', 'Capital One', 'SunTrust', 'BB&T Bank', 'Santander Bank', 'Regions Bank', 'Fifth Third Bank', 'KeyBank', 'Ally Bank']
    name = random.choice(names)
    bank_name = random.choice(bank_names)
    
    data = {
        'human_name': name,
        'bank_name': bank_name,
    }
    
    return data