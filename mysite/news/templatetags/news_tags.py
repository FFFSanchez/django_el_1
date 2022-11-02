from django import template
from django.db.models import Count, F
from news.models import Category
from django.core.cache import cache

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Hello', arg2='Sidebar'):
    categories = cache.get('categories')  # пытаемся получить данные из кеша
    if not categories:  # если в кеше нет то получаем их из БД
        categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
        cache.set('categories', categories, 30)  # и кладем в кеш на 30 сек
    # cache.get_or_set('my_new_key', 'my new value', 100) # или так в одну строку
    # categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)

    return {'categories': categories, 'arg1': arg1, 'arg2': arg2}


