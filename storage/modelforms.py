'''
Created on 28/giu/2016

@author: sabah
'''

from models import BackendUsed
from django.forms import Form
from django import forms
from captcha.fields import ReCaptchaField


class SelectBEForm(Form):
    def __init__(self, *args, **kwargs):
        super(SelectBEForm, self).__init__(*args, **kwargs)
        self.fields['codBE'] = forms.CharField(widget=forms.Select(choices=self.return_be_list()), label="Back End")
        self.fields['pagination_number'] = forms.IntegerField(
            widget=forms.Select(choices=[(x, str(x)) for x in range(25, 501, 25)]), label="Results for page")

    def return_be_list(self):
        be_list_choise = [(x.backend, x.backend) for x in self.initial["backends"]]
        return be_list_choise

    codBE = forms.CharField(
        widget=forms.Select(choices=[(x.backend, x.backend) for x in BackendUsed.objects.all()]),
        label="Back End")
    pagination_number = forms.IntegerField(widget=forms.Select(choices=[(x, str(x)) for x in range(25, 501, 25)]),
                                           label="Results for page")
    source_name = forms.CharField(required=False, max_length=100, label="Source Name")
    frequency_min = forms.CharField(required=False, max_length=100, label="Frequency min (MHz)")
    frequency_max = forms.CharField(required=False, max_length=100, label="Frequency max (MHz)")
    pointing_position_ra = forms.CharField(required=False, max_length=100, label="Pointing Position ra (deg)")
    pointing_position_dec = forms.CharField(required=False, max_length=100, label="Pointing Position dec (deg)")
    pointing_position_radius = forms.CharField(required=False, max_length=100, label="Pointing Position radius (deg)")


class VerifyHuman(Form):
    def __init__(self, *args, **kwargs):
        super(VerifyHuman, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField()

    def clean(self):
        cleaned_data = super(VerifyHuman, self).clean()
        return cleaned_data
