import csv, os, django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User,Group

file_path = 'user.csv'

def import_users(file_path):
    with open(file_path, encoding='utf-8')as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            fio_parts = row['ФИО'].split(' ')
            last_name = fio_parts[0]
            first_name = fio_parts[1]
            email_parts = row['Логин'].split('@')
            user_name = email_parts[0]


            user,created =User.objects.get_or_create(
                username=user_name,
                defaults={
                    'email': row['Логин'],
                    'first_name':first_name,
                    'last_name': last_name,
                    'is_staff':row['Роль сотрудника'] in ['Администратор','Менеджер'],
                    'is_superuser':row['Роль сотрудника'] in ['Администратор']
                }
            )

            if created:
                user.set_password(row['Пароль'])
                user.save()

                role_name= row['Роль сотрудника']
                group, _ = Group.objects.get_or_create(name=role_name)
                user.groups.add(group)

                print(f"Пользователь {user.username} создан с ролью {role_name}")
            else:
                print(f"Пользователь {user.username} уже существует")

import_users(file_path)