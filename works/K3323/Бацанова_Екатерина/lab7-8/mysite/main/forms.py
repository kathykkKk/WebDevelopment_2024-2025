from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Comment
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient

class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Ваш email')
    subject = forms.CharField(label='Тема', max_length=200)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'rows': 6, 'cols': 40}))

class RecipeForm(forms.ModelForm):
    instructions = forms.CharField(
        widget=CKEditor5Widget(config_name='default')
    )

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'cook_time_hours',
            'cook_time_minutes',
            'active_time_hours',
            'active_time_minutes',
            'instructions',
            'image',
            'category',
        ]

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'weight', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Наименование',
                'required': True,
                'class': 'ingredient-input'
            }),
            'weight': forms.TextInput(attrs={
                'placeholder': 'Вес (г)',
                'class': 'ingredient-input'
            }),
            'quantity': forms.TextInput(attrs={
                'placeholder': 'Количество',
                'class': 'ingredient-input'
            }),
        }

IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=1,
    can_delete=True
)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите комментарий...'})
        }
