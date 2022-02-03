from django.urls import path
from userincome.views import index, add_income, income_edit, delete_income, search_income,\
    income_test, add_income_test, export_csv_income, export_excel_income, \
    export_pdf_income, income_details


from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name="income"),
    path('add-income/', add_income, name="add-income"),
    path('edit-income/<int:id>/', income_edit, name="income-edit"),
    path('income-delete/<int:id>/', delete_income, name="income-delete"),
    path('search-income/', csrf_exempt(search_income), name="search_income"),
    path('search-income_test/', income_test, name="income_test"),
    path('add_income_test/', add_income_test, name="add_income_test"),
    path('export_csv_income/', export_csv_income, name="export_csv_income"),
    path('export_excel_income/', export_excel_income, name="export_excel_income"),
    path('export_pdf_income/', export_pdf_income, name="export_pdf_income"),
    path('income_details/<int:id>/', income_details, name="income_details"),
]