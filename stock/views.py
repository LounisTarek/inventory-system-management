from django.forms import ModelForm
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
import datetime

from django.db import transaction
# Create your views here.
def home(request):
    invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')
    page_num = request.GET.get("page")
    paginator = Paginator(invoices, 8)
    try:
        invoices = paginator.page(page_num)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    context = {
        'invoices': invoices,
    }

    if request.POST.get('id_modified'):

        paid = request.POST.get('modified')

        try:

            obj = Invoice.objects.get(id=request.POST.get('id_modified'))

            if paid == 'True':

                obj.paid = True

            else:

                obj.paid = False

            obj.save()

            messages.success(request, "Change made successfully")

        except Exception as e:

            messages.error(request, f"Sorry, the following error has occured {e}.")

    return render(request, 'dashboared.html', context)

def AddCustomer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        user = request.user

        created = Customer.objects.create(save_by=user,name=name,email=email,phone=phone,adresse=address,sex=sex,age=age,city=city,zip_code=zip)
        if created:
            messages.success(request, "customer created successfully")
            return redirect('home')

        else:
            messages.error(request, "please try again")
            return redirect('home')

    return render(request, 'addcustomer.html')

def AddInvoice(request):
    customers = Customer.objects.select_related('save_by').all()

    context = {
        'customers': customers
    }

    if request.method == 'POST':

        items = []

        try:

            customer = request.POST.get('customer')

            type = request.POST.get('invoice_type')

            articles = request.POST.getlist('article')

            qties = request.POST.getlist('qty')

            units = request.POST.getlist('unit')

            total_a = request.POST.getlist('total-a')

            total = request.POST.get('total')

            comment = request.POST.get('commment')

            invoice_object = {
                'customer_id': customer,
                'save_by': request.user,
                'total': total,
                'invoice_type': type,
                'comments': comment
            }

            invoice = Invoice.objects.create(**invoice_object)

            for index, article in enumerate(articles):
                data = Article(
                    invoice_id=invoice.id,
                    name=article,
                    quantity=qties[index],
                    unit_price=units[index],
                    total=total_a[index],
                )

                items.append(data)

            created = Article.objects.bulk_create(items)

            if created:
                messages.success(request, "Data saved successfully.")
            else:
                messages.error(request, "Sorry, please try again the sent data is corrupt.")

        except Exception as e:
            messages.error(request, f"Sorry the following error has occured {e}.")

    return render(request, 'addinvoice.html', context)


def delete(request, pk):
    obj = Invoice.objects.get(id=pk)
    obj.delete()
    messages.success(request, "the invoice deleted successfully")
    return redirect('home')

def ViewInvoice(request, pk):
    obj = Invoice.objects.get(id=pk)
    articles = obj.article_set.all()
    context = {
        'obj': obj,
        'articles': articles
    }
    return render(request, "viewinvoice.html", context)

def InvoicePdf(request, pk):

    obj = Invoice.objects.get(id=pk)
    articles = obj.article_set.all()
    context = {
        'obj': obj,
        'articles': articles,
    }

    # get html file
    template = get_template('invoice-pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format

    # generate pdf

    pdf = pdfkit.from_string(html, False, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response





