from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expense/', views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>/', views.expense_edit, name="expense-edit"),
    path('expense-delete/<int:id>/', views.delete_expenses, name="expense-delete"),
    path('search-expenses/', csrf_exempt(views.search_expenses),
         name="search_expenses"),
    path('expense_category_summary/', views.expense_category_summary,
         name="expense_category_summary"),
    path('stats/', views.stats_view,
         name="stats"),
    path('delete_expenses/<int:id>/', views.delete_expenses, name='delete_expenses'),
    path('test', views.test, name='test'),
    path('test_pie', views.test_pie, name='test_pie'),
    path('export_csv', views.export_csv, name='export-csv'),
    path('export_excel', views.export_excel, name='export-excel'),
    path('export_pdf', views.export_pdf, name='export_pdf'),
    path('details/<int:id>/', views.get_details, name='get_details'),
]