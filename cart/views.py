from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Cart, CartItem, Order, OrderItem
from .forms import AddToCartForm, CheckoutForm
from products.models import Product


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += form.cleaned_data['quantity']
            cart_item.save()
            return redirect('view_cart')
    else:
        form = AddToCartForm(initial={'product': product})
    return render(request, 'cart/add_to_cart.html', {'form': form, 'product': product})


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    return render(request, 'cart/view_cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total': sum(item.total_price for item in cart_items)
    })


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required
@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return redirect('view_cart')
    cart_item.save()
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                shipping_address=f"{form.cleaned_data['street_address']}, {form.cleaned_data['city']}, {form.cleaned_data['state']}, {form.cleaned_data['postal_code']}, {form.cleaned_data['country']}",
                total_price=sum(item.product.price * item.quantity for item in cart.items.all()),
                payment_method=form.cleaned_data['payment_method']
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart.items.all().delete()
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, 'cart/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_status.html', {'order': order})


@login_required
def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.is_admin or request.user.is_moderator:
        if request.method == 'POST':
            order.status = request.POST.get('status')
            order.save()
            return redirect('order_status', order_id=order.id)
    return render(request, 'orders/change_order_status.html', {'order': order})


@login_required
def order_history(request):
    if request.method == 'POST' and (request.user.is_admin or request.user.is_moderator):
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        return redirect('order_history')

    if request.user.is_admin or request.user.is_moderator:
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order.shipping_address = f"{form.cleaned_data['street_address']}, {form.cleaned_data['city']}, {form.cleaned_data['state']}, {form.cleaned_data['postal_code']}, {form.cleaned_data['country']}"
            order.payment_method = form.cleaned_data['payment_method']
            order.save()
            return redirect('order_status', order_id=order.id)
    else:
        form = CheckoutForm(initial={
            'street_address': order.user.street_address,
            'city': order.user.city,
            'state': order.user.state,
            'postal_code': order.user.postal_code,
            'country': order.user.country,
            'payment_method': order.payment_method
        })
    return render(request, 'cart/order_confirmation.html', {'order': order, 'form': form})
