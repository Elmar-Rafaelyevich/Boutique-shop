from django.urls import path
from shop.views import (Index, SubCategories, ProductPage, 
                        login_registration, user_login, user_logout, 
                        registration, save_review)

urlpatterns = [
    # class view
    path('', Index.as_view(), name='index'),
    path('category/<slug:slug>/', SubCategories.as_view(), name='category_detail'),
    path('product_page/<slug:slug>/', ProductPage.as_view(), name='product_page'),

    # func view
    path('login_registration/', login_registration, name='login_registration'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', registration, name='registration'),
    path('save_review/<int:product_pk>', save_review, name='save_review'),

]
