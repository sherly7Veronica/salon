from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
import json
import stripe
from django.http.response import HttpResponseNotFound, JsonResponse
from django.urls import reverse, reverse_lazy

from django.contrib import messages
# from .models import Transaction
# from app import generate_checksum, verify_checksum

User = get_user_model()
  
def homePage(request) : 
    return render(request ,  "app/homePage.html" )

from .forms import RegisterForm

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'app/register.html', { 'form': form})  

    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'app/register.html', {'form': form})    

class ProductListView(ListView):
    model = Product   
    template_name = 'app/product_list.html'
    context_object_name = 'product_list'

    
class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = "app/product_create.html"
    success_url = reverse_lazy("home-page")

class ProductDetailView(DetailView):
    model = Product
    template_name = "app/product_detail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context  

@csrf_exempt
def create_checkout_session(request, id):

    request_data = json.loads(request.body)
    product = get_object_or_404(Product, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email = request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        # success_url=request.build_absolute_uri(
        #     reverse('success')
        # ) + "?session_id={CHECKOUT_SESSION_ID}",
        # cancel_url=request.build_absolute_uri(reverse('failed')),
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price * 100)
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})

class PaymentSuccessView(TemplateView):
    template_name = "app/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = "app/payment_failed.html"

class OrderHistoryListView(ListView):
    model = OrderDetail
    template_name = "app/order_history.html"

from .resources import OrderResource
from .models import OrderDetail
from django.http import HttpResponse

def export_data(request):
    if request.method == "POST":
        file_format = request.POST['file-format']
        order_resource = OrderResource()
        dataset = order_resource.export()

        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment'; filename = "order_data.csv"
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment'; filename = "order_data.json"
            return response
        if file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment'; filename = "order_data.xls"
            return response

    return render(request, 'export.html')