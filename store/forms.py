from django import forms

class EmailForms(forms.Form):
    email = forms.EmailField(required=True)
    product = forms.CharField(required=True)