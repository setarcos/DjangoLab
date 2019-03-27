#-*- coding: UTF-8 -*-

from django import forms

class LendForm(forms.Form):
    username = forms.CharField(
        label='姓名',
        error_messages={'required': '姓名必须填写'} # don't work for hint messages?
        )
    telephone = forms.CharField(
        label='电话',
        )
    note = forms.CharField(
        label='备注',
        )

class NewItem(forms.Form):
    itemname = forms.CharField(
        label = '设备名称',
        )
    serial = forms.CharField(
        label = '序列号',
        )
    value = forms.CharField(
        label = '价格',
        )
    room = forms.CharField(
        label = '所在房间号',
        )
    note = forms.CharField(
        required = False,
        label = '备注',
        widget = forms.Textarea(),
        )
