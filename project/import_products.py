import os, csv, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from project_app.models import *
file_path = 'products.csv'

def import_products(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f,delimiter=',')
        for row in reader:
            u, _ = Unit.objects.get_or_create(name=row['Единица измерения'])
            s, _ = Supplier.objects.get_or_create(name=row['Поставщик'])
            m, _ = Manufacturer.objects.get_or_create(name=row['Производитель'])
            c, _ = Category.objects.get_or_create(name=row['Категория товара'])

            Product.objects.update_or_create(
                sku=row['Артикул'],
                defaults={
                    'name': row['Наименование товара'],
                    'price': int(row['Цена']),
                    'unit': u,
                    'supplier': s,
                    'manufacturer': m,
                    'category': c,
                    'discount': int(row['Действующая скидка']),
                    'stock': int(row['Кол-во на складе']),
                    'description': (row['Описание товара']),
                    'image': (row['Фото'])
                }
            )
if __name__ == "__main__":
    import_products(file_path)