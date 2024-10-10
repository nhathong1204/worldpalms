$(document).ready(function() {
    // add to cart 
    $(document).on('click','.add-to-cart-btn', function(){
        let this_val = $(this)
        let index = this_val.data('index')

        let quantity = $('.product-quantity-'+ index).val()
        let product_title = $('.product-title-'+ index).val()
        let product_id = $('.product-id-'+ index).val()
        let product_pid = $('.product-pid-'+ index).val()
        let product_image = $('.product-image-'+ index).val()
        let product_price = $('.current-product-price-'+ index).val()
        
        console.log('quantity',quantity)
        console.log('product_title',product_title)
        console.log('product_id',product_id)
        console.log('product_pid',product_pid)
        console.log('product_image',product_image)
        console.log('product_price',product_price)
        console.log('index',index)

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'title': product_title,
                'image': product_image,
                'qty': quantity,
                'price': product_price,
            },
            dataType: 'json',
            success: function(res){
                btn_name = this_val.html()
                this_val.html('✔')
                setTimeout(function(){
                    this_val.html(btn_name)
                },2000)
                console.log('Product added successfully')
                $('.cart-items-count').text(res.totalcartitems)
                if(res.cart_store) {
                    $('#cart-store').html('')
                    $('#cart-store').html(res.cart_store)

                    $(".bb-side-cart-overlay, .bb-cart-close").on("click", function (e) {
                        e.preventDefault();
                        $(".bb-side-cart-overlay").fadeOut();
                        $(".bb-side-cart").removeClass("bb-open-cart");
                    });

                    $(".cart-remove-item").on("click", function (e) {
                        $(this).parents(".cart-sidebar-list").remove();
                        var wish_product_count = $(".cart-sidebar-list").length;
                        if (wish_product_count == 0) {
                            $('.bb-cart-items').html('<p class="bb-wishlist-msg">Your Cart is empty!</p>');
                        }
                    });
                }
            }
        })
    })

    $(document).on('click', '.delete-product', function(){
        let product_id = $(this).data('product')
        $('li.cart-sidebar-list').each(function(){
            cart_product_id = $(this).find('a.delete-product').data('product')
            if(cart_product_id == product_id) {
                $(this).closest('li').remove()
            }
        })

        $.ajax({
            url: '/delete-from-cart',
            data: {
                'id': product_id
            },
            dataType: 'json',
            success: function(res) {
                $('.cart-items-count').text(res.totalcartitems)
                $('#cart-list').html('')
                $('#cart-list').html(res.data)
            }
        })
    })

    $(document).on('click', '.qty-plus-minus .bb-qtybtn', function(){
        let product_id = $(this).closest('tr').data('product')
        let this_val = $(this)
        let product_quantity = $('.product-quantity-'+product_id).val()
        $.ajax({
            url: '/update-cart',
            data: {
                'id': product_id,
                'qty': product_quantity,
            },
            dataType: 'json',
            success: function(res) {
                $('.cart-items-count').text(res.totalcartitems)
                $('#cart-list').html('')
                $('#cart-list').html(res.data)
            }
        })
    })

    $(document).on('submit','#contact-form-ajax',function(e){
        e.preventDefault()
        console.log('Submited...')
        let first_name = $('#first_name').val()
        let last_name = $('#last_name').val()
        let email = $('#email').val()
        let phone = $('#phone').val()
        let subject = $('#subject').val()
        let message = $('#message').val()

        $.ajax({
            url: '/ajax-contact-form',
            data: {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
            },
            dataType: 'json',
            success: function(res) {
                console.log('Sent data to server...')
                console.log('Sent data to server...')
                if(res.success == true) {
                    $('#contact-form-ajax').hide()
                    $('#message_sent').text(res.message)
                }
            }
        })
    })

    $(document).on('submit','#place-order-ajax',function(e){
        e.preventDefault()
        console.log('Submited...')
        let cartData = [];

        $('tr[data-product]').each(function() {
            let product_id = $(this).data('product');
            let title = $('.item-title-' + product_id).val();
            let price = $('.item-price-' + product_id).val();
            let qty = $('.item-qty-' + product_id).val();
            let subtotal = $('.item-subtotal-' + product_id).val();

            cartData.push({
                'product_id': product_id,
                'title': title,
                'price': price,
                'qty': qty,
                'subtotal': subtotal,
            });
        });
        let full_name = $('#full_name').val()
        let email = $('#email').val()
        let phone = $('#phone').val()
        let city = $('#city').val()
        let district = $('#district').val()
        let ward = $('#ward').val()
        let address = $('#address').val()
        let total_amount = $('.total_amount').val()

        $.ajax({
            url: '/ajax-place-order',
            data: {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'city': city,
                'district': district,
                'ward': ward,
                'address': address,
                'total_amount': total_amount,
                'cart_data': JSON.stringify(cartData),
            },
            dataType: 'json',
            success: function(res) {
                console.log('Sent data to server...')
                console.log('Sent data to server...')
                if(res.success == true) {
                    $('#cart-list').html("")
                    $('#cart-list').html('<p class="text-success" id="message_sent" style="text-align: center; font-size: 20px; font-weight: bold;">'+res.message+'</p>')
                }
            }
        })
    })
})