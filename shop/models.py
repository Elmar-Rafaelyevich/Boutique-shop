from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование категории')
    image = models.ImageField(upload_to='categories_photo/', verbose_name='Изображение', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Категория', related_name='subcategories')


    def get_absolute_url(self):
        # ссылка на страницу категории
        return reverse(viewname='category_detail', kwargs={'slug':self.slug})
    

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return f'Категория pk={self.pk} title={self.title}'
    
    def get_parent_category_photo(self):
        if self.image:
            return self.image.url
        else:
            return "https://admiral.digital/wp-content/uploads/2023/08/404_page-not-found.png"
        

    class Meta:
        verbose_name='Категория'
        verbose_name_plural ='Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование товара')
    price = models.FloatField(verbose_name='Цена', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    watched = models.IntegerField(default=0, verbose_name='Просмотры')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    desc = models.TextField(default='Нет описания', verbose_name='Описание товара')
    info = models.TextField(default='Дополнительная информация', verbose_name='Информация о товаре')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name='Размер в мм')
    color = models.CharField(default='Чёрный', max_length=25, verbose_name='Цвет/Материал')


    def get_absolute_url(self):
          # ссылка на страницу категории
        return reverse(viewname='product_page', kwargs={'slug':self.slug})
    
    def get_first_photo(self):
        if self.images.first():
            return self.images.first().image.url 
        else:
            return "https://admiral.digital/wp-content/uploads/2023/08/404_page-not-found.png"
        
    def __str__(self):
        return self.title
    
    def __repr__(self):
        return f'Категория pk={self.pk} title={self.title} price={self.price}'
    

    class Meta:
        verbose_name='Товар'
        verbose_name_plural ='Товары'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='images')
    
    class Meta:
        verbose_name='Изображение'
        verbose_name_plural ='Галерея товаров'

CHOICES = (
    ("5", "Отлично"),
    ("4", "Хорошо"),
    ("3", "Нормально"),
    ("2", "Плохо"),
    ("1", "Ужасно"),
)

class Review(models.Model):
    # comment
    text = models.TextField(verbose_name='Комментария')
    grade = models.CharField(max_length=20, choices=CHOICES, blank=True, null=True, verbose_name='Оценка')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Продукт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    def __str__(self):
        # имя автора 
        return self.author.username
    
    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural ='Отзывы'
