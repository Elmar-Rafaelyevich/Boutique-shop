from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from random import randint
from django.contrib.auth import login, logout
from django.contrib import messages


# local .py
from shop.models import Category, Product
from shop.forms import LoginForm, RegistrationForm


class Index(ListView):
    # Главная стр

    model = Product
    template_name = "shop/index.html"
    context_object_name = 'categories'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['top_products'] = Product.objects.order_by('-watched')[:8]

        return context

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories
    

class SubCategories(ListView):
    model = Product
    context_object_name = 'products' 
    template_name = 'shop/category_page.html'

    def get_queryset(self):
        type_field = self.request.GET.get('type')
        if type_field:
            products = Product.objects.filter(category__slug=type_field)
            return products
        
        
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = parent_category.subcategories.all()
        products = Product.objects.filter(category__in=subcategories).order_by("?")

        if sort_field := self.request.GET.get('sort'):
            products = products.order_by(sort_field)
        return products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        context['category']  = parent_category
        context['title'] = parent_category.title
        return context
     

class ProductPage(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs['slug'])

        data = Product.objects.all().exclude(slug=self.kwargs['slug']).filter(category=product.category)[:5]

        context['title']= product.title
        context['products'] = data
        return context
    
def login_registration(request):
    context = {'title':'Войти или зарегистрироваться',
               'login_form':LoginForm,
               'registration_form':RegistrationForm
               }
    
    return render(request, 'shop/login_registration.html', context)


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, 'Введённый пароль или имя не верный')
        return redirect('login_registration')
    

def user_logout(request):
    logout(request)
    return redirect('index')


def registration(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Аккаунт пользователя успешно создан')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())
        # messages.error(request, 'Что-то пошло не так')

    return redirect('login_registration')
    