from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import requests
from account.models import Customer
import uuid
from store.models import *
from .models import *
from hubtel.views import send_link
# Create your views here.


def exchanged_rate(amount):
    url = "https://www.blockonomics.co/api/price?currency=USD"
    r = requests.get(url)
    response = r.json()
    return amount/response['price']
@login_required
def track_invoice(request, pk):
    invoice_id = pk
    invoice = Invoice.objects.get(id=invoice_id)
    data = {
            'order_id':invoice.order_id,
            'bits':invoice.btcvalue/1e8,
            'value':invoice.product.price,
            'addr': invoice.address,
            'status':Invoice.STATUS_CHOICES[invoice.status+1][1],
            'invoice_status': invoice.status,
        }
    if (invoice.received):
        data['paid'] =  invoice.received/1e8
        if (int(invoice.btcvalue) <= int(invoice.received)):
            send_link(request,product_id=invoice.product.id)
            if invoice.product.category.name == "Extraction":
                pass
            else:
                invoice.product.Status = False
                invoice.product.save()
            return render(request, 'account/registration/buy_email_confirm.html')
    else:
        data['paid'] = 0  

    return render(request,'invoice.html',context=data)
@login_required
def create_payment(request, pk):
    
    product_id = pk
    product = Product.objects.get(id=product_id)
    url = 'https://www.blockonomics.co/api/new_address'
    headers = {'Authorization': "Bearer " + settings.API_KEY}
    r = requests.post(url, headers=headers)
    if r.status_code == 200:
        address = r.json()['address']
        bits = exchanged_rate(product.price)
        order_id = uuid.uuid1()
        invoice = Invoice.objects.create(order_id=order_id,
                                address=address,btcvalue=bits*1e8, product=product, created_by=request.user)
        return HttpResponseRedirect(reverse('payment:track_payment', kwargs={'pk':invoice.id}))
    else:
        print(r.status_code, r.text)
        return HttpResponse("Some Error, Try Again!")
    
def receive_payment(request):
    
    if (request.method != 'GET'):
        return 
    
    txid  = request.GET.get('txid')
    value = request.GET.get('value')
    status = request.GET.get('status')
    addr = request.GET.get('addr')

    invoice = Invoice.objects.get(address = addr)
    
    invoice.status = int(status)
    if (int(status) == 2):
        invoice.received = value
        invoice.sold = True
        
    invoice.txid = txid
    invoice.save()
    return HttpResponse(200)


#User balance codes
@login_required
def add_balance(request):
    api_key = 'x3ji0hvKMvtHuDTdEnLbyAA9adz501I10gXP7FgNxCE'
    amount = float(1.00)
    url = 'https://www.blockonomics.co/api/new_address'
    headers = {'Authorization': "Bearer " + api_key}
    r = requests.post(url, headers=headers)
    if r.status_code == 200:
        address = r.json()['address']
        bits = exchanged_rate(amount)
        order_id = uuid.uuid1()
        # Check if the user already has a balance model
        balance = Balance.objects.filter(created_by=request.user).first()
        if balance:
            # If the user has a balance model, use its id
            invoice_id = balance.id
            balance.address = address
            balance.received = 0
            balance.save()
        else:
            # Otherwise, create a new balance model
            invoice = Balance.objects.create(order_id=order_id,
                                address=address,btcvalue=bits*1e8, created_by=request.user)
            invoice_id = invoice.id
        return HttpResponseRedirect(reverse('payment:track_balance', kwargs={'pk': invoice_id}))

    else:
        print(r.status_code, r.text)
        return HttpResponse("Some Error, Try Again!")
@login_required
def track_balance(request, pk):
    invoice_id = pk
    invoice = Balance.objects.get(id=invoice_id)
    data = {
            'order_id':invoice.order_id,
            'bits':invoice.btcvalue/1e8,
            'value':invoice.balance,
            'addr': invoice.address,
            'status':Balance.STATUS_CHOICES[invoice.status+1][1],
            'invoice_status': invoice.status,
        }
     
    if (invoice.received):
            
        data['paid'] =  invoice.received/1e8
        if (int(invoice.btcvalue) <= int(invoice.received)):
            return redirect('home')
    else:
         data['paid'] = 0  

    return render(request,'invoice.html',context=data)

def receive_balance(request):
    if request.method == 'GET':
        txid = request.GET.get('txid')
        value = float(request.GET.get('value'))
        status = request.GET.get('status')
        addr = request.GET.get('addr')

        invoice = Balance.objects.get(address=addr)
        
        if int(status) == 2:
            invoice.status = int(status)
            invoice.received = value
            invoice.txid = txid
            invoice.balance = 0
            invoice.save()

            # update user's balance
            received = float(invoice.received)
            url = "https://www.blockonomics.co/api/price?currency=USD"
            response = requests.get(url).json()
            usdvalue = received / 1e8 * response["price"]
            invoice.balance += usdvalue
            invoice.save()

        return HttpResponse(status=200)
    else:
        return HttpResponseBadRequest()

#Buying
@login_required
def buy(request,pk):
    product_id = pk
    product = Product.objects.get(id=product_id)
    price = product.price
    balance = Balance.objects.filter(created_by=request.user).first()
    if balance:
        b = balance.balance
        if b is not None:
            remaining = int(price - b)
        else:
            balance.balance = 0
            balance.save()
            remaining = int(price - balance.balance)
        if remaining < 0:
            remaining = 0
    else:
        remaining = price
    if request.method == "POST":
        balance = Balance.objects.filter(created_by=request.user).first()
        if balance:
            b = balance.balance
            check = int(price - b)
            if check > 0:
                return redirect("payment:create_balance")
            else:
                balance.balance = b - price
                balance.save()
                
                invoice = Invoice.objects.create(status=2,order_id=balance.order_id,
                                address=balance.address,btcvalue=balance.btcvalue, product=product, 
                                created_by=request.user,sold=True,received=balance.received)
                send_link(request,product_id=product_id)
                if product.category.name == "Extraction":
                    pass
                else:
                    product.Status = False
                    product.save()
                return render(request, 'account/registration/buy_email_confirm.html')
        else:
            return redirect("payment:create_balance")
    return render(request,'buy.html',context={"price":price,"remain":remaining,"product":product})

#chatBot activation
@login_required
def create_payment_bot(request):
    api = 'Xaw6hOuwdBoNocLEHJNottYixVhRlKbmjuvl5rPn9NA'
    amount = 50
    url = 'https://www.blockonomics.co/api/new_address'
    headers = {'Authorization': "Bearer " + api}
    r = requests.post(url, headers=headers)
    if r.status_code == 200:
        address = r.json()['address']
        bits = exchanged_rate(amount)
        order_id = uuid.uuid1()
        chat = ChatBot.objects.create(order_id=order_id,
                                address=address,btcvalue=bits*1e8,user=request.user)
        return HttpResponseRedirect(reverse('payment:track_payment_bot', kwargs={'pk':chat.id}))
    else:
        print(r.status_code, r.text)
        return HttpResponse("Some Error, Try Again!")
@login_required   
def track_invoice_bot(request, pk):
    chat_id = pk
    chat = ChatBot.objects.get(id=chat_id)
    user = chat.user
    data = {
            
            'bits':chat.btcvalue/1e8,
            'invoice_status': chat.status,
            'addr': chat.address,
        }
    if (chat.received):
        
        if (int(chat.btcvalue) <= int(chat.received)):
            user.verified = True
            user.save()
            return redirect('home')
    return render(request, 'invoice.html',context=data)

def receive_balance_bot(request):
    if request.method == 'GET':
        txid = request.GET.get('txid')
        value = float(request.GET.get('value'))
        status = request.GET.get('status')
        addr = request.GET.get('addr')

        chat = ChatBot.objects.get(address=addr)
        
        if int(status) == 2:
            chat.status = int(status)
            chat.received = value
            chat.txid = txid
            chat.save()

        return HttpResponse(status=200)
    else:
        return HttpResponseBadRequest()