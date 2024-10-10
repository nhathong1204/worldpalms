import json
from django.shortcuts import render
from core.models import Product
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def index(request):
    context = {}
    return render(request, 'core/index.html',context)

def product_list_view(request):
    product_list = Product.objects.filter(product_status="published").order_by('-id')
    total_products = product_list.count()
    page = request.GET.get('page',1)
    paginator = Paginator(product_list,10)
    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        products = paginator.page(1)
    context = {
        'products': products,
        'total_products': total_products,
    }
    return render(request, 'core/product-list.html',context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    
    productRelated = Product.objects.filter(product_status="published", category=product.category).exclude(pid=pid)
    p_image = product.p_images.all()
    context = {
        'product': product,
        'p_image': p_image,
        'productRelated': productRelated,
    }
    return render(request, 'core/product-detail.html',context)

def add_to_cart(request):
    cart_product = {}
    cart_product[request.GET.get('id')] = {
        'title': request.GET.get('title'),
        'qty': request.GET.get('qty'),
        'price': request.GET.get('price'),
        'image': request.GET.get('image'),
        'title': request.GET.get('title'),
        'pid': request.GET.get('pid'),
    }
    

    if 'cart_data_obj' in request.session:
        if str(request.GET.get('id')) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[request.GET.get('id')]['qty'] = int(cart_product[request.GET.get('id')]['qty']) + int(cart_data[request.GET.get('id')]['qty'])
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product


    # add cart data to menu top
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
            sub_total = 0
            for p_id, item in request.session['cart_data_obj'].items():
                sub_total = int(item['qty']) * float(item['price'])
                cart_total_amount += sub_total
                request.session['cart_data_obj'][p_id]['subtotal'] = sub_total
                request.session.modified = True
    cart_store = render_to_string('core/async/cart-store.html', {'cart_total_amount': cart_total_amount,'cart_data':request.session['cart_data_obj']})
    #end add cart data to menu top
        
    context = {
        'data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_store': cart_store,
    }
        
    return JsonResponse(context)


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        context = {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
        }
        return render(request, 'core/cart.html',context)
    else:
        context = {
            'cart_data': '',
            'totalcartitems': 0,
            'cart_total_amount': cart_total_amount,
        }
        return render(request, 'core/cart.html',context)


def update_cart(request):
    product_id = request.GET.get('id')
    product_qty = request.GET.get('qty')
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            # cart_data = request.session['cart_data_obj']
            # cart_data[request.GET.get('id')]['qty'] = product_qty
            # cart_data.update(cart_data)
            request.session['cart_data_obj'][request.GET.get('id')]['qty'] = product_qty
            request.session['cart_data_obj'][request.GET.get('id')]['subtotal'] = int(product_qty)*float(request.session['cart_data_obj'][request.GET.get('id')]['price'])
            request.session.modified = True
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string('core/async/cart-list.html', {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
        })
    return JsonResponse({'data': context,'totalcartitems': len(request.session['cart_data_obj'])})

def delete_item_from_cart(request):
    product_id = request.GET.get('id')
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            del request.session['cart_data_obj'][product_id]
            request.session.modified = True
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string('core/async/cart-list.html', {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
        })
    return JsonResponse({'data': context,'totalcartitems': len(request.session['cart_data_obj'])})


def search_view(request):
    query = request.GET.get('q')
    category = request.GET.get('cat')
    if category == "all":
        product_list = Product.objects.filter(title__icontains=query,product_status="published").order_by('-date')
    else:
        product_list = Product.objects.filter(title__icontains=query,product_status="published",category=category).order_by('-date')
    total_products = product_list.count()
    page = request.GET.get('page',1)
    paginator = Paginator(product_list,10)
    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        products = paginator.page(1)
    context = {
        'products': products,
        'category': category,
        'total_products': total_products,
        'query': query,
    }
    return render(request, 'core/search.html', context)

def about_us(request):
    return render(request, 'core/about_us.html')

def contact_us(request):
    return render(request, 'core/contact_us.html')

def ajax_contact_form(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    subject = request.GET.get('subject')
    message = request.GET.get('message')
    
    from_email = settings.DEFAULT_FROM_EMAIL
    context = {
        'user': request.user,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'subject': subject,
        'subject': subject,
        'message': message
    }
    email_template = 'emails/contact_email_template.html'
    message = render_to_string(email_template, context)
    to_email = settings.ADMIN_EMAIL
    mail = EmailMessage(subject, message, from_email, to=[to_email])
    mail.send()
    
    return JsonResponse({
        'success': True,
        'message': ' Message sent successfully.'
    })

def ajax_place_order(request):
    cart_data = json.loads(request.GET.get('cart_data'))
    
    from_email = settings.DEFAULT_FROM_EMAIL
    context = {
        'user': request.user,
        'full_name': request.GET.get('full_name') or None,
        'email': request.GET.get('email') or None,
        'phone': request.GET.get('phone') or None,
        'city': request.GET.get('city') or None,
        'district': request.GET.get('district') or None,
        'ward': request.GET.get('ward') or None,
        'address': request.GET.get('address') or None,
        'total_amount': request.GET.get('total_amount') or 0,
        'cart_data': cart_data or [],
    }
    email_template = 'emails/place_order_template.html'
    
    message = render_to_string(email_template, context)
    to_email = settings.ADMIN_EMAIL
    subject = f"Place order from user: {request.user.username}"
    mail = EmailMessage(subject, message, from_email, to=[to_email])
    mail.send()
    
    return JsonResponse({
        'success': True,
        'message': ' Place Order Successfully. We will contact you soon. Thanks!!!'
    })