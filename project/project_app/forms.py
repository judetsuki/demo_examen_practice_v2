from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if self.instance and self.instance.pk:
            self.fields['id'] = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required = False    , initial = self.instance.pk)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'