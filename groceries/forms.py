#-*- coding: UTF-8 -*-

from django import forms

class LendForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u'姓名',
        error_messages={'required': '请输入姓名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u'姓名',
            }
        ),
    )
    telephone = forms.CharField(
        required=True,
        label=u'电话',
        error_messages={'required': '请输入联系方式'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u'电话',
            }
        ),
    )
