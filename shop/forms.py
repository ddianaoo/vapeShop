from django import forms
from .models import Category


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'slug',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': "Назва",
            'slug': "Назва для пошуку(Slug)",
        }