from django.contrib import admin
from shop.models import Product, Category, Gallery, Review
from django.utils.safestring import mark_safe

class GalleryInline(admin.TabularInline):
    model=Gallery
    extra=3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_product_count')
    # гинерация slug 
    prepopulated_fields = {'slug':('title',)}

    def get_product_count(self, obj):
        return str(obj.products.count())
            
    # Меняю названи поле в админке с get_product_count на Кол-во товаров
    get_product_count.short_description = 'Кол-во товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # выведи мне эти данный в админке 
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'color', 'size', 'get_photo')
    # динамические данные
    list_editable = ('price', 'quantity', 'size', 'color')
    # создание slug
    prepopulated_fields = {'slug': ('title',)}
    #  фильтрация по полям название товара и по цене
    list_filter = ('title', 'price')
    # создаёт ссылку для полей 'pk', 'title'
    list_display_links = ('pk', 'title')
    readonly_fields = ('watched',)
    # ссылка для загрузки изображения товара 
    inlines = (GalleryInline,)

    # Функция которая добавляет изображения в админке 
    def get_photo(self, obj_photo):
        if obj_photo.images.all():
            # width=70 это оптимальный размер товаров а АДМИНКЕ
            return mark_safe(f'<img src="{obj_photo.images.all()[0].image.url}" width="70">')

        else:
            # при отсутствие изображения товара выводит слово 'Нет изображение'
            return 'Нет изображение'
    # параметр short_description() меняет название функции с get_photo на Изображения товара
    get_photo.short_description = 'Изображения товара'


@admin.register(Review)
class ReviwAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'created_at')
    readonly_fields = ('author', 'text', 'created_at')


admin.site.register(Gallery)