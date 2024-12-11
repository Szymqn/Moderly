from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Cart, CartItem, Order, OrderItem
from .forms import AddToCartForm
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
    cart = Cart.objects.get(user=request.user)
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
        order = Order.objects.create(
            user=request.user,
            shipping_address=f"{request.user.street_address}, {request.user.city}, {request.user.state}, {request.user.postal_code}, {request.user.country}",
            total_price=sum(item.product.price * item.quantity for item in cart.items.all())
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()
        return redirect('order_status', order_id=order.id)
    return render(request, 'cart/view_cart.html', {'cart': cart})


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
