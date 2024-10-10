from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    #Home page
    path('', views.index, name='index'),
    
    # Products page
    path('products/', views.product_list_view, name='product-list'),
    path('product/<pid>/', views.product_detail_view, name='product-detail'),
    
    # add to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    # delete item from cart
    path('delete-from-cart/', views.delete_item_from_cart, name='delete-from-cart'),
    
    # cart page
    path('place-order/', views.cart_view, name='place-order'),
    
    # update cart
    path('update-cart/', views.update_cart, name='update-cart'),
    
    # search
    path('search/', views.search_view, name='search'),
    
    # Other pages
    path('about-us/', views.about_us, name='about-us'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('ajax-contact-form/', views.ajax_contact_form, name='ajax-contact-form'),
    path('ajax-place-order/', views.ajax_place_order, name='ajax-place-order'),

]
