from import_export import resources
from .models import OrderDetail


class OrderResource(resources.ModelResource):
    class Meta:
        model = OrderDetail
