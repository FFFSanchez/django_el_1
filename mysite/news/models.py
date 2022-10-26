from django.db import models
from django.urls import reverse

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование') # макс длина поля
    content = models.TextField(blank=True) # поле можно оставить пустым
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано') # устанавливает now дату 1 раз
    updated_at = models.DateTimeField(auto_now=True) #обновляет дату каждый раз
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'news_id': self.pk}) # название маршрута и параметры для его построения

    #def my_func(self):
        #return 'Hello from model'

    def __str__(self):  # магический метод возвр строковое представление объекта
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at', 'title'] # критерии сортировки


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk}) # название маршрута и параметры для его построения

    def __str__(self):  # магический метод возвр строковое представление объекта
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title'] # критерии сортировки