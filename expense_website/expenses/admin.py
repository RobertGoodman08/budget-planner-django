from django.contrib import admin
from expenses.models import Expense, Category


admin.site.register(Expense)
admin.site.register(Category)