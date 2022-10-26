from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import News, Category
# Create your views here.


def index(request):
    #print(request)
    news = News.objects.all()  #order_by('-created_at')   # с сортировкой, но можно просто .all()
    #categories = Category.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
        #'categories': categories,
    }
    return render(request, template_name='news/index.html', context=context) # именованые, можно позиционные

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    #categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    context = {
        'news': news,
        #'categories': categories,
        'category': category,
    }
    return render(request, 'news/category.html', context) # именованые, можно позиционные

def view_news(request, news_id):    # news_id как и category_id мы получаем из urls.py path:...
    #news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    context = {
        'news_item': news_item,
    }
    return render(request, 'news/view_news.html', context)




#def test(request):
#    return HttpResponse('<h1>Test sOplii</h1>')