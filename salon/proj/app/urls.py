from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	# path('hello/', views.HelloView.as_view(), name ='hello'),
	# path('superadmin/', superadmin.site.urls),
	# path('register/',views.register,name="register"),
	path('', views.homePage, name ='home-page'),
	# path('user/', views.user, name ='user'),
	# path('teacher/', views.teacher, name ='teacher'),
	# path('register/', RegisterView.as_view(template_name="app/loginPage.html"), name ='login-user'),
	path('register/', views.sign_up, name='register'),
	path('login/', LoginView.as_view(template_name="app/loginPage.html"), name ='login-user'),
	path('logout/', LogoutView.as_view(template_name="app/logoutPage.html"), name ='logout'),
	path('product_list/', views.ProductListView.as_view(template_name="app/product_list.html"), name ='product_list'),
	path('detail/<id>/', views.ProductDetailView.as_view(), name='detail'),
	path('payment_success/', views.PaymentSuccessView.as_view(template_name="app/payment_success.html"), name='payment_success'),
    path('failed/', views.PaymentFailedView.as_view(), name='failed'),
    path('history/', views.OrderHistoryListView.as_view(), name='history'),
	path('create/', views.ProductCreateView.as_view(), name='create'),

    path('api/checkout-session/<id>/', views.create_checkout_session, name='api_checkout_session'),
]	
