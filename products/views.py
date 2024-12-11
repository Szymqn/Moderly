from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Comment
from cart.models import Cart, CartItem
from .form import CommentForm, ProductDescriptionForm


def product_list(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = int(request.POST.get('quantity', 1))
        else:
            cart_item.quantity += int(request.POST.get('quantity', 1))
        cart_item.save()
        return redirect('view_cart')

    return render(request, 'products/products.html', {'products': products, 'categories': categories})


def product_detail(request, product_id):
    current_user = request.user if request.user.is_authenticated else None
    product = get_object_or_404(Product, id=product_id)
    form = CommentForm()
    description_form = None

    if current_user and (current_user.is_admin or
                         str(current_user.category) == str(product.category)):
        if request.method == 'POST' and 'description_form' in request.POST:
            description_form = ProductDescriptionForm(request.POST, instance=product)
            if description_form.is_valid():
                description_form.save()
                return redirect('product_detail', product_id=product.id)
        else:
            description_form = ProductDescriptionForm(instance=product)

    if request.method == 'POST' and 'comment_form' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id=product.id)

    if request.method == 'POST' and 'quantity' in request.POST:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = int(request.POST['quantity'])
        else:
            cart_item.quantity += int(request.POST['quantity'])
        cart_item.save()
        return redirect('view_cart')

    all_comments = Comment.objects.filter(product=product)
    valid_comments = []
    permission_comments = []

    for comment in all_comments:
        if (str(current_user.category) == str(product.category) or
                current_user.is_admin is True or
                comment.user == current_user or
                comment.approved is True):
            valid_comments.append(comment)
            if str(current_user.category) == str(product.category) or current_user.is_admin is True:
                permission_comments.append(comment)

    return render(request, 'products/product_detail.html',
                  {
                      'product': product,
                      'comments': valid_comments,
                      'form': form,
                      'description_form': description_form,
                      'permission_comments': permission_comments,
                  })


@login_required
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.approved = True
    comment.save()
    return redirect('product_detail', product_id=comment.product.id)
