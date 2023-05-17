from django import forms
from .models import Clients, Mailing, Messages

class ClientsForm(forms.Form):
    class Meta:
        phone = forms.IntegerField()
        teg = forms.CharField(required=False)
        code_operator = forms.IntegerField(min_value=800, max_value=999)
        time_zone = forms.IntegerField(required=False)


class MailingForm(forms.ModelForm):
    start_mailing = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M', '%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M', ])
    finish_mailing = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M', '%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M', ])

    class Meta:
        model = Mailing
        fields = (
            'finish_mailing', 'start_mailing', 'text_message')
        widgets = {
            'text_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }