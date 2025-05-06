# Create your views here.
from .models import Category
from .forms import RecipeForm, RegisterForm
from .forms import ContactForm
from .models import ContactMessage
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from .models import RecipeLike
from .forms import CommentForm
from django.shortcuts import render, redirect
from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientForm
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Comment

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


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('recipe_list')
        else:
            return render(request, 'main/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def recipe_create(request):
    IngredientFormSet = modelformset_factory(Ingredient, form=IngredientForm, extra=1)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            # Сохраняем рецепт
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            # Сохраняем ингредиенты
            for ingredient_form in formset:
                if ingredient_form.cleaned_data and not ingredient_form.cleaned_data.get('DELETE', False):
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()

            return redirect('recipe_list')
    else:
        form = RecipeForm()
        formset = IngredientFormSet(queryset=Ingredient.objects.none())

    # Отключаем required у шаблона пустой формы
    for field in formset.empty_form.fields.values():
        field.required = False

    return render(request, 'main/recipe_form.html', {
        'form': form,
        'formset': formset
    })

from django.db.models import Q
from django.shortcuts import render
from .models import Recipe, Category

from django.db.models import Q
from .models import Recipe, Category, Ingredient

def recipe_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    ingredient_input = request.GET.get('ingredient', '')
    exclude_input = request.GET.get('exclude_ingredient', '')

    include_ingredients = [i.strip().lower() for i in ingredient_input.split(',') if i.strip()]
    exclude_ingredients = [i.strip().lower() for i in exclude_input.split(',') if i.strip()]

    recipes = Recipe.objects.all()

    # Фильтрация по поисковому запросу (название или описание)
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Фильтрация по категории
    if category_id:
        recipes = recipes.filter(category_id=category_id)

    # Фильтрация по включённым ингредиентам
    for ing in include_ingredients:
        recipes = recipes.filter(ingredients__name__iexact=ing)

    # Исключение по ингредиентам
    for ing in exclude_ingredients:
        recipes = recipes.exclude(ingredients__name__iexact=ing)

    # Исключаем дубликаты рецептов после JOIN’ов
    recipes = recipes.distinct()

    # Получаем все категории для формы
    categories = Category.objects.all()

    return render(request, 'main/recipe_list.html', {
        'recipes': recipes,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'ingredient': ingredient_input,
        'exclude_ingredient': exclude_input,
    })

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.filter(parent__isnull=True).order_by('-created_at')
    is_liked = False
    if request.user.is_authenticated:
        is_liked = RecipeLike.objects.filter(user=request.user, recipe=recipe).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.recipe = recipe
            new_comment.user = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                new_comment.parent_id = int(parent_id)
            new_comment.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = CommentForm()

    return render(request, 'main/recipe_detail.html', {
        'recipe': recipe,
        'is_liked': is_liked,
        'form': form,
        'comments': comments
    })


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, RecipeLike, Comment


@login_required
def recipe_like(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Проверяем, есть ли уже лайк от пользователя
    like, created = RecipeLike.objects.get_or_create(user=request.user, recipe=recipe)

    if not created:
        # Если лайк уже есть, удаляем его
        like.delete()
        liked = False
    else:
        liked = True

    # Пересчитываем лайки после изменения
    total_likes = recipe.total_likes()

    # Если запрос AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': total_likes,
        })

    # Перенаправляем на страницу рецепта
    return redirect('recipe_detail', pk=pk)


@login_required
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    # Если пользователь уже поставил лайк, удаляем его
    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True

    # Пересчитываем лайки после изменения
    total_likes = comment.total_likes()

    # Если запрос AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': total_likes,
        })

    # Перенаправляем на страницу рецепта
    return redirect('recipe_detail', pk=comment.recipe.pk)

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        messages.error(request, "Вы не можете редактировать чужой рецепт.")
        return redirect('recipe_list')

    IngredientFormSet = modelformset_factory(Ingredient, form=IngredientForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSet(request.POST, request.FILES, queryset=recipe.ingredients.all())

        if form.is_valid() and formset.is_valid():
            form.save()

            # Обновляем ингредиенты
            for ingredient_form in formset:
                if ingredient_form.cleaned_data.get('DELETE'):
                    if ingredient_form.instance.pk:
                        ingredient_form.instance.delete()
                else:
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.recipe = recipe
                    ingredient.save()

            messages.success(request, "Рецепт успешно обновлён!")
            return redirect('recipe_detail', pk=recipe.pk)
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
    else:
        form = RecipeForm(instance=recipe)
        formset = IngredientFormSet(queryset=recipe.ingredients.all())

    # Чтобы не было ошибок required у пустой формы (если вдруг будет extra > 0)
    for field in formset.empty_form.fields.values():
        field.required = False

    return render(request, 'main/recipe_form.html', {
        'form': form,
        'formset': formset,
        'recipe': recipe,
    })


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        messages.error(request, "Вы не можете удалить чужой рецепт.")
    else:
        recipe.delete()
        messages.success(request, "Рецепт успешно удалён.")
    return redirect('recipe_list')

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'main/my_recipes.html', {'recipes': recipes})
