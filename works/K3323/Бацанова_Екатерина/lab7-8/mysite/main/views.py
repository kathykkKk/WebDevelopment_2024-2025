from django.shortcuts import render
from .forms import ContactForm
from django.contrib import messages
from .models import ContactMessage

def home_view(request):
    return render(request, 'main/home.html')

def about_view(request):
    return render(request, 'main/about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохраняем данные в базу
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Сообщение отправлено!')
            form = ContactForm()  # очистить форму
        else:
            # Вывод ошибок формы, если они есть
            messages.error(request, 'Произошла ошибка при отправке сообщения.')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

