from core.models import Product
from django.db.models import Min,Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.shortcuts import get_current_site

def default(request):
    current_site = get_current_site(request)
    query_selected = None
    if request.GET.get('q'):
        query_selected = request.GET.get('q')
    
    product_list = Product.objects.filter(product_status="published").order_by('date')
    total_products = product_list.count()
    page = request.GET.get('page',1)
    paginator = Paginator(product_list,20)
    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        products = paginator.page(1)

    min_max_price = Product.objects.aggregate(Min('price'),Max('price'))

    #get cart
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        
        cart_data = request.session['cart_data_obj']
    else:
        cart_data = ''
    
    return {
        'query_selected': query_selected,
        'products': products,
        'total_products': total_products,
        'min_max_price': min_max_price,
        'cart_data': cart_data,
        'cart_total_amount': cart_total_amount,
    }