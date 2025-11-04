"""URL patterns for the Checkout app with trailing slashes."""
from django.urls import path

from .views import (
    api_canceled_order_service_view,
    api_confirm_order_service_view,
    api_customer_portal_view,
    api_detail_order_view,
    api_order_service_view,
    api_pay_Money_view,
    api_purchase_orders_view,
    api_pawn_Money_view,
    api_renew_service_view,
    api_requested_orders_view,
    api_subscription_detail_webhook,
    api_subscription_view,
)

app_name = "checkout"

urlpatterns = [
    path("pawn/", api_pawn_Money_view, name="pawnMoney"),
    path("renew/", api_renew_service_view, name="renewService"),
    path("subscribe/", api_subscription_view, name="subscribe"),
    path("order/", api_order_service_view, name="orderService"),
    path("confirm/", api_confirm_order_service_view, name="confirmedOrderService"),
    path("canceled/", api_canceled_order_service_view, name="canceledOrderService"),
    path("pay/", api_pay_Money_view, name="payOwnerService"),
    path("orderDetail/<pk>/", api_detail_order_view, name="orderDetail"),
    path("purchaseOrders/", api_purchase_orders_view.as_view(), name="purchaseOrders"),
    path("requestedOrders/", api_requested_orders_view.as_view(), name="requestedOrders"),
    path("webhook/", api_subscription_detail_webhook, name="webhook"),
    path("customerPortal/", api_customer_portal_view, name="customerPortal"),
]
