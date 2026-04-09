import os, csv, django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from project_app.models import *
file_path = 'order.csv'

def parse_date(date_str):
    for fmt in ('%m/%d/%Y', '%d.%m.%Y'):
        try:
            return datetime.strptime(date_str,fmt).date()
        except ValueError:
            continue
    return None

def import_orders(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')

        for row in reader:
            dp, _ = DeliveryPoint.objects.get_or_create(address=row['Адрес пункта выдачи'])
            o_date = parse_date(row['Дата заказа'])
            d_date = parse_date(row['Дата доставки'])

            if o_date is None or d_date is None:
                print(f"propusk stroki")
                continue

            order = Order.objects.create(
                order_date=o_date,
                delivery_date=d_date,
                status=row['Статус заказа'],
                receiver_name=row['ФИО авторизированного клиента'],
                delivery_code=row['Код для получения'],
                delivery_address=dp
            )

            data = [i.strip() for i in row['Артикул заказа'].split(',')]
            for i in range(0,len(data),2):
                OrderDetail.objects.create(
                    order=order,
                    product=Product.objects.get(sku=data[i]),
                    order_quantity=int(data[i+1])
                )

if __name__ == "__main__":
    import_orders(file_path)

