from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    sku = models.CharField(max_length=100,unique=True,verbose_name='Артикул')
    name = models.CharField(max_length=255,verbose_name='Наименование')
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Цена')
    unit = models.ForeignKey('Unit',on_delete=models.PROTECT,related_name='products',verbose_name='Единица Измерения')
    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT,related_name='products',verbose_name = 'Поставщик')
    manufacturer = models.ForeignKey('Manufacturer', on_delete = models.PROTECT,related_name='products',verbose_name='Производитель')
    category = models.ForeignKey('Category', on_delete= models.PROTECT,related_name='products',verbose_name='Категория')
    discount = models.PositiveIntegerField(default=0,verbose_name='Скидка')
    stock = models.PositiveBigIntegerField(default=0,verbose_name='Количество на складе')
    description = models.TextField(verbose_name='Описание')
    image = models.CharField(max_length=255,blank=True)
    def __str__(self):
        return f"{self.sku} | {self.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('completed', 'завершен'),
        ('new', 'новый')
    ]
    orderDate = models.DateField(verbose_name='Дата заказа')
    deliveryDate = models.DateField(verbose_name='Дата доставки')
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, verbose_name='Статус заказа')
    deliveryAddress = models.ForeignKey('DeliveryPoint', on_delete=models.CASCADE,verbose_name='Адрес пункта выдачи')
    receiver_name = models.TextField(verbose_name='Имя получателя')
    deliveryCode = models.TextField('Код для получения')
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='orders',null=True, blank=True,verbose_name='Клиент',)

class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE,related_name='items',verbose_name='Заказ')
    product = models.ForeignKey('Product', on_delete=models.PROTECT,verbose_name='Товар')
    order_quantity = models.PositiveIntegerField(default=1,verbose_name='Кол-во')
    

class Supplier(models.Model):
    name = models.CharField(max_length=40) #не добавлял def __str__(self): и verbose чтобы посмотреть как будет отличаться

class Category(models.Model):
    name = models.CharField(max_length=40,verbose_name='Категория')
    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class DeliveryPoint(models.Model):
    address = models.CharField(max_length=255)
    def __str__(self):
        return self.address

class Unit(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name
    