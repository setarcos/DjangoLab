from django import forms
from .models import Survey

class PubkeyForm(forms.Form):
    stu_id = forms.CharField(
        label='学号',
        widget=forms.TextInput(attrs={'readonly':True}),
        )
    pubkey = forms.CharField(
        label='公钥'
        )
