from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Product(models.Model):
    sku = models.CharField(max_length=100,unique=True,verbose_name='Артикул')
    name = models.CharField(max_length=255,verbose_name='Наименование')
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Цена')
    unit = models.CharField(max_length=20,default = 'шт.',verbose_name='Единица Измерения') 
    supplier = models.CharField(max_length=100,verbose_name = 'Поставщик')
    manufacturer = models.CharField(max_length=100,verbose_name='Производитель')
    category = models.CharField(max_length=100,verbose_name='Категория') 
    discount = models.PositiveIntegerField(default=0,verbose_name='Скидка')
    stock = models.PositiveBigIntegerField(default=0,verbose_name='Количество на складе')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images/',max_length=255,blank=True, null=True,verbose_name='Изображение')
    def __str__(self):
        return f"{self.sku} | {self.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Завершен', 'Завершен'),
        ('Новый', 'Новый')
    ]
    order_number = models.CharField(max_length=20,unique=True,verbose_name="Номер Заказа")
    order_date = models.DateField(verbose_name='Дата заказа')
    delivery_date = models.DateField(verbose_name='Дата доставки')
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, verbose_name='Статус заказа')
    delivery_address = models.ForeignKey('DeliveryPoint', on_delete=models.CASCADE,verbose_name='Адрес пункта выдачи')
    delivery_code = models.CharField(max_length=30,verbose_name='Код для получения')
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='orders',null=True, blank=True,verbose_name='Клиент',)
    def __str__(self):
        return str(self.pk)

class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE,related_name='items',verbose_name='Заказ')
    product = models.ForeignKey('Product', on_delete=models.PROTECT,verbose_name='Товар')
    order_quantity = models.PositiveIntegerField(default=1,verbose_name='Кол-во')
    def __str__(self):
        return str(self.order)
    
class DeliveryPoint(models.Model):
    address = models.CharField(max_length=255)
    def __str__(self):
        return self.address

    