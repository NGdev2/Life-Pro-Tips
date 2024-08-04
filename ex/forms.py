from django import forms
from .models import Tip

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control tip-textarea', 'style': 'height: 100px;'})
        }
