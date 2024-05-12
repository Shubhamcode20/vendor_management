from django.urls import path
from . import views

urlpatterns = [
    path('api/vendors/', views.VendorApi.as_view()),
    path('api/vendors/<int:vendor_id>/', views.VendorApi.as_view()),
    path('api/vendors/<int:vendor_id>/performance/', views.VendorPerformanceApi.as_view()),
    path('api/purchase-orders/', views.PurchaseOrderApi.as_view()),
    path('api/purchase-orders/<int:purchase_order_id>/', views.PurchaseOrderApi.as_view()),
    path('api/purchase-orders/<int:purchase_order_id>/acknowledge/', views.PurchaseOrderAcknowledgeApi.as_view())
]
