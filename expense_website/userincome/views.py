from django.shortcuts import render, redirect, get_object_or_404
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Avg, Min, Max
import json
import csv
import datetime
import xlwt



def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency

    current_user = request.user
    shopcart = UserIncome.objects.filter(owner_id=current_user.id)

    income_total = UserIncome.objects.filter(owner=request.user).aggregate(min_amount=Min('amount'),
                                                                          avg_amount=Avg('amount'),
                                                                          max_amount=Max('amount'))

    total = 0
    for rs in shopcart:
        total += rs.amount


    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
        'total': total,
        'income_total': income_total,
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date,
                                  source=source, description=description)
        messages.success(request, 'Record saved successfully')

        return redirect('income')


@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)
        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('income')

@login_required(login_url='/user/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'record removed')
    return redirect('income')


def income_test(request):
    income = UserIncome.objects.filter(owner=request.user).order_by('-date')

    context = {
        'income': income
    }
    return render(request, 'income_test.html', context)



def add_income_test(request):
    income_pie = UserIncome.objects.filter(owner=request.user)

    context = {
        'income_pie': income_pie
    }

    return render(request, 'add_income_test.html', context)



def export_csv_income(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Expenses' + str(datetime.datetime.now())+'.csv'

    response.write(u'\ufeff'.encode('utf8'))
    writer =csv.writer(response)
    writer.writerow(['Сумма', 'Источник', 'Описание', 'Дата'])

    expenses=UserIncome.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.source, expense.description, expense.date])


    return response


def export_excel_income(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Сумма', 'Описание', 'Источник', 'Дата']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = UserIncome.objects.filter(owner=request.user).values_list(
        'amount', 'description', 'source', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def export_pdf_income(request):
    return render(request, 'income/pdf-output-income.html')


def income_details(request, id):
    income = get_object_or_404(UserIncome, id=id)

    context = {
        'income': income
    }

    return render(request, 'income/income_details.html', context)