from .models import Category
from payment.models import *
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
        