from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.encoding import  force_str
from django.utils.http import urlsafe_base64_decode
from .forms import RegistrationForm
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
            phone_number = registerForm.cleaned_data["mobile"]
            country_choice = registerForm.cleaned_data["country_choice"]
            
            if country_choice == 'US':
                phone_number = "+1" + phone_number
                user.mobile = phone_number
            elif country_choice == 'GH':
                phone_number = "+233" + phone_number
                user.mobile = phone_number
            elif country_choice == 'CA':
                phone_number = "+1" + phone_number
                user.mobile = phone_number
            if country_choice == 'DE':
                phone_number = "+49" + phone_number
                user.mobile = phone_number
            if country_choice == 'AU':
                phone_number = "+61" + phone_number
                user.mobile = phone_number

            user.email = registerForm.cleaned_data["email"]
            email = registerForm.cleaned_data["email"]
            user.user_name = registerForm.cleaned_data["user_name"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            # Rest of the code...
            request.session['user_id'] = user.id
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

