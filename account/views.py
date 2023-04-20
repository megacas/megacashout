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
@login_required
def dashboard(request):
    return render(request, "account/dashboard/dashboard.html", {"section": "profile", })


@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "edit-details.html", {"user_form": user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


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
            user.is_active = True
            user.save()
            login(request, user)
            users = Customer.objects.get(email=email)
            send_otp(users,phone_number)
            return redirect("otp_form")
    else:
        registerForm = RegistrationForm()
    return render(request, "signup.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")

#@login_required
#def user_orders(request):
    #user_id = request.user.id
    #orders = Order.objects.filter(user_id=user_id)[0:5]
    #return render(request, "account/dashboard/user_orders.html", {"orders": orders})
