import os
import django

# Налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_record_store.settings')
django.setup()

from persistence import context

# Функція для демонстрації роботи репозиторіїв
def demonstrate_repositories():
    # Додамо нову роль співробітника
    new_role = context.EmployeeRoleContext().create(rolename='Manager_helper') # Створення екземпляра
    print(f"Added new role: {new_role.rolename}")

    # Додамо нового співробітника
    new_employee = context.EmployeeContext().create(
        emp_name='Maria',
        last_name='Brychko',
        username='mashka',
        phonenumber='3942572458',
        age=18,
        emp_password='123456',
        email='maria@example.com',
        address='126 Main St',
        role=new_role
    )
    print(f"Added new employee: {new_employee.emp_name} {new_employee.last_name}")
