from django.contrib import admin
from app.models import *
from import_export.admin import ExportActionMixin


class ProductAdminSite(admin.AdminSite):
    list_display = ('email',)
    site_header = "Super Admin"
    site_title = "Super Admin Portal"
    index_title = "Welcome to SuperAdmin page"

super_admin_site = ProductAdminSite(name='post_admin')    
 
class OrderDetailAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('product', 'amount')


admin.site.register(Teacher)
admin.site.register(Student)

super_admin_site.register(UserAccount)
super_admin_site.register(OrderDetail, OrderDetailAdmin)
super_admin_site.register(Product)