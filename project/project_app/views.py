from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
# Create your views here.

def delete_order(request,pk):
    if request.user.is_superuser:
        get_object_or_404(Order,pk=pk).delete()
    return redirect('product_list')

def delete_product(request,pk):
    if request.user.is_superuser:
        get_object_or_404(Product,pk=pk).delete()
    return redirect('product_list')

def edit_product(request,pk):
    if request.user.is_superuser:
        product = get_object_or_404(Product,pk=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render (request, 'store/edit_form.html', {'form':form, 'title':'редактирование товара'})

def product_list(request):
    user = request.user
    products = Product.objects.all()
    orders = []

    if user.is_staff:
        search_query=request.GET.get('search')
        if search_query:
            products=products.filter(name__icontains=search_query)
        orders = Order.objects.all()
        #менеджер только видит заказы
    # if user.is_superuser:
        
     #логика удаления заказов

    return render (request, 'store/product_list.html',{
        'products': products,
        'orders': orders,
    })