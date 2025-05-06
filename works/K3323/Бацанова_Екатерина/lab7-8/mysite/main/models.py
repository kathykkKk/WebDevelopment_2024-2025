# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    subject = models.CharField(max_length=255, default='No subject')  # Set a default value for 'subject'
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name="Автор")
    title = models.CharField(max_length=200, verbose_name="Название рецепта")
    description = models.TextField(verbose_name="Описание")
    instructions = CKEditor5Field('Инструкции', config_name='default')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True, verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes", verbose_name="Категория")
    cook_time_hours = models.PositiveIntegerField(default=0, verbose_name="Время готовки (часы)")
    cook_time_minutes = models.PositiveIntegerField(default=0, verbose_name="Время готовки (минуты)")
    active_time_hours = models.PositiveIntegerField(default=0, verbose_name="Ваше время (часы)")
    active_time_minutes = models.PositiveIntegerField(default=0, verbose_name="Ваше время (минуты)")

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100, verbose_name="Наименование")
    weight = models.CharField(max_length=100, blank=True, null=True, verbose_name="Вес (г)")
    quantity = models.CharField(max_length=100, blank=True, null=True, verbose_name="Количество")

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.quantity or '-'} шт, {self.weight or '-'} г)"

class RecipeLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

class Comment(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def total_likes(self):
        return self.likes.count()

    def user_liked(self, user):
        return self.likes.filter(id=user.id).exists()

    def __str__(self):
        return f"Комментарий от {self.user.username} к рецепту {self.recipe.title}"
