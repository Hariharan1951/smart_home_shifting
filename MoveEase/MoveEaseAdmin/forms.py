from django import forms
from .models import CouponCodeTable

class CouponCodeTaleForm(forms.ModelForm):

    class Meta():
        model = CouponCodeTable
        fields = "__all__"