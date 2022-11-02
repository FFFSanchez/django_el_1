from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # была UserCreationForm
        if form.is_valid():
            # form.save()
            user = form.save() # сразу присвоить  данные чтобы сразу залогинится
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            # return redirect('login')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'news/register.html', context)

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'hello world from MyMixin'
    # extra_context = {'title': 'Главная'}
    #queryset = News.objects.select_related('category')
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False     # дает 404 для несуществующих
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    #template_name = 'news/news_detail.html' #  и так используеца по умолчанию
    #pk_url_kwarg = 'news_id'

class CreateNews(LoginRequiredMixin, CreateView):
    login_url = '/admin/' # или на главную reverse_lazy('home')
    #raise_exception = True   # error 403
    form_class = NewsForm
    template_name = 'news/add_news.html'
    #success_url = reverse_lazy('home') # вместо get_absolute_url


def mail_test(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'django.fff@mail.ru', ['lordsanchez@yandex.ru'], fail_silently=True)
            if mail: # send_mail возвращает кол-во отправок 0 или другое число
                messages.success(request, 'Письмо отправлено')
                return redirect('mail_test')
            else:
                messages.error(request, 'Ошибка отправки - fail_silently=True')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'news/mail_test.html', context)


def test(request):
    objects = [
    ' El Page1',' El Page2',' El Page3',' El Page4',' El Page5',' El Page6', ' El Page7'
    ]
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)   # 1 если не будет параметра page в GET
    page_objects = paginator.get_page(page_num) # get_page возвращет послденюю страницу если запрошена страница большая чем ваще доступна
    context = {
        'page_obj': page_objects
    }
    return render(request, 'news/test.html', context)



# def index(request):
#     #print(request)
#     news = News.objects.all()  #order_by('-created_at')   # с сортировкой, но можно просто .all()
#     #categories = Category.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#         #'categories': categories,
#     }
#     return render(request, template_name='news/index.html', context=context) # именованые, можно позиционные

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     #categories = Category.objects.all()
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         #'categories': categories,
#         'category': category,
#     }
#     return render(request, 'news/category.html', context) # именованые, можно позиционные

# def view_news(request, news_id):    # news_id как и category_id мы получаем из urls.py path:...
#     #news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item,
#     }
#     return render(request, 'news/view_news.html', context)

# def add_news(request):
#     if request.method == 'POST': # а это видимо когда жмешь кнопку в уже заполненой форме
#         form = NewsForm(request.POST) # связанная с данными форма в любом случае если ПОСТ
#         if form.is_valid():
#             #print(form.cleaned_data)
#             #news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             #return redirect('home')
#             return redirect(news)
#     else:
#         form = NewsForm()     # не связанная с данными форма если ГЕТ
#                               # видимо это просто открыть форму это гет
#     context = {
#         'form': form   # либо связанная с данными либо нет будет зависит ПОСТ или ГЕТ
#     }
#     return render(request, 'news/add_news.html', context)




#def test(request):
#    return HttpResponse('<h1>Test sOplii</h1>')