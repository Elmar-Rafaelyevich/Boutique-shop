from shop.models import  Category
from django import template



register = template.Library()


@register.simple_tag()
def get_subcategory(category):
    return Category.objects.filter(parent=category)


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title':'Цена',
            'sorters':[
                ('price', 'по возрастанию'),
                ('-price', 'по убыванию')
            ]

        },
        {
            'title':'Цвет',
            'sorters':[
                ('color', 'от А до Я'),
                ('-color', 'от Я до А')
            ]
        },
        {
            'title':'Размер',
            'sorters':[
                ('size', 'по возрастанию'),
                ('-size', 'по убыванию')
            ]
        }
    ]
    return sorters
