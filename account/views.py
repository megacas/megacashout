from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from store.models import Product
#from order.models import Order
from .forms import RegistrationForm,  UserEditForm
from .models import  Customer
from .tokens import account_activation_token
from hubtel.views import send_otp
from django.contrib.auth import login
from payment.models import *
@login_required
def dashboard(request):
    user = request.user
    invoice = Invoice.objects.filter(sold=True,created_by=user)
    data = {
        "products":invoice
    }
    return render(request, "account/user/dashboard.html", context=data)

def account_register(request):

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            phone_number = str("+233"+str(registerForm.cleaned_data["mobile"]))
            user.email = registerForm.cleaned_data["email"]
            email = registerForm.cleaned_data["email"]
            user.user_name = registerForm.cleaned_data["user_name"]
            user.mobile = registerForm.cleaned_data["mobile"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            users = Customer.objects.get(email=email)
            if send_otp(request,users,phone_number):
                return redirect("otp_form")
            else:
                return render(request, 'account/registration/register_email_confirm.html',{'mobile':user.mobile})
            
    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/signup.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("home")
    else:
        return render(request, "account/registration/activation_invalid.html")

