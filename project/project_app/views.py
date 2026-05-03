from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from .models import *
from .forms import *
# Create your views here.

def delete_order(request,pk):
    if request.user.is_superuser:
        get_object_or_404(Order,pk=pk).delete()
    return redirect('project_app:product_list')

def delete_product(request,pk):
    if request.user.is_superuser:
        get_object_or_404(Product,pk=pk).delete()
    return redirect('project_app:product_list')

def create_product(request):
    if not request.user.is_superuser:
        return redirect('project_app:product_list')
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('project_app:product_list')
    else:
        form = ProductForm()
    return render (request,'store/form_generic.html', {'form':form, 'title':'создание продукта'})

def edit_product(request,pk):
    if not request.user.is_superuser:
        return redirect('project_app:product_list')
    
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('project_app:product_list')
    else:
        form = ProductForm(instance=product)
    return render (request, 'store/form_generic.html', {'form':form, 'title':'редактирование продукта'})

def edit_order(request,pk):
    if not request.user.is_superuser:
        return redirect('project_app:product_list')
    
    order = get_object_or_404(Order,pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('project_app:product_list')
    else:
        form = OrderForm(instance=order)
    return render (request, 'store/form_generic.html', {'form':form, 'title':'редактирование заказов'})


def product_list(request):
    user = request.user
    products = Product.objects.all()
    orders = []
    suppliers = Product.objects.values_list('supplier', flat = True).distinct()

    if user.is_authenticated and (user.is_staff or user.is_superuser):
        search_query=request.GET.get('search')
        if search_query:
            products=products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(manufacturer__icontains=search_query) |
                Q(supplier__icontains=search_query)
                )

        supplier_filter = request.GET.get('supplier')
        if supplier_filter:
            products=products.filter(supplier=supplier_filter)

        sort_by = request.GET.get('sort')
        if sort_by in ['stock','-stock',]:
            products = products.order_by(sort_by)


        orders = Order.objects.all()

    return render (request, 'store/product_list.html',{
        'products': products,
        'orders': orders,
        'suppliers': suppliers,
    })