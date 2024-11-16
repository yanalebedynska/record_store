import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_project.settings')
django.setup()

from pharmacyApp.repositories.employee_repository import EmployeeRepository
from pharmacyApp.repositories.customer_repository import CustomerRepository
from pharmacyApp.repositories import context


def add_employee():

    new_employee = context.EmployeeRepository().create(
        name = 'Nastia Borsch',
        position = 'Manager',
        hire_date = '2020-12-12',
        salary = 1350.00,
        birthday_date = '2006-09-13'
    )
    print(f"Added new employee: {new_employee.name} - {new_employee.position}")

def add_customer():

    new_customer = context.CustomerRepository().create(
        name = 'Olena',
        email = 'olena@gmail.com',
        phone_number = '068 552 57 07',
        address = 'Some address',
    )
    print(f"Added new customer: {new_customer.name}")


def delete_employee(employee_id):

    employee_repository = EmployeeRepository()
    deleted_employee = employee_repository.delete_by_id(employee_id)

    if deleted_employee:
        message = f"Employee with ID {employee_id} is deleted successfully"
    else:
        message = f"Employee with ID {employee_id} isn't found"

    print(message)


def delete_customer(customer_id):

    customer_repository = CustomerRepository()
    deleted_customer = customer_repository.delete_by_id(customer_id)

    if deleted_customer:
        message = f"Customer with ID {customer_id} is deleted successfully"
    else:
        message = f"Customer with ID {customer_id} isn't found"

    print(message)


def display_all_employees():

    print("\nList of all employees:")
    for employee in context.EmployeeRepository().get_all():
        print(f"ID: {employee.employee_id}, Name: {employee.name}, Position: {employee.position}")

def display_all_customers():

    print("\nList of all customers:")
    for customer in context.CustomerRepository().get_all():
        print(f"ID: {customer.customer_id}, Name: {customer.name}")


if __name__ == "__main__":
    #delete_customer(1)
    add_customer()
    display_all_customers()
    add_employee()
    #delete_employee(2)
    display_all_employees()