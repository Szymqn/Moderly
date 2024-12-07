from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Comment
from .form import CommentForm


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

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = CommentForm()

    all_comments = Comment.objects.all()
    valid_comments = []
    permission_comments = []

    for comment in all_comments:
        if (str(current_user.category) == str(product.category) or
                current_user.is_admin is True or
                comment.user == current_user or
                comment.approved is True
        ):
            valid_comments.append(comment)
            if str(current_user.category) == str(product.category) or current_user.is_admin is True:
                permission_comments.append(comment)

    return render(request, 'products/product_detail.html',
                  {
                      'product': product,
                      'comments': valid_comments,
                      'form': form,
                      'permission_comments': permission_comments,
                  })


@login_required
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.approved = True
    comment.save()
    return redirect('product_detail', product_id=comment.product.id)
