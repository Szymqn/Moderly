from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Comment


def product_list(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/products.html', {'products': products, 'categories': categories})


def product_detail(request, product_id):
    current_user = request.user if request.user.is_authenticated else None
    product = get_object_or_404(Product, id=product_id)

    all_comments = Comment.objects.all()
    valid_comments = []

    for comment in all_comments:
        if (str(current_user.category) == str(product.category) or
                current_user.is_admin is True or
                comment.user == current_user or
                comment.approved is True
        ):
            valid_comments.append(comment)

    return render(request, 'products/product_detail.html',
                  {'product': product,
                   'comments': valid_comments})
