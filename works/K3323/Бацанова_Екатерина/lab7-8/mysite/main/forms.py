from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Ваш email')
    subject = forms.CharField(label='Тема', max_length=200)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'rows': 6, 'cols': 40}))


