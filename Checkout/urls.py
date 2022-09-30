from django.urls import path
from .views import(

	api_canceled_order_service_view,
	api_detail_order_view,
	api_purchase_orders_view,
	api_requested_orders_view,
	api_pawn_Money_view,
	api_order_service_view,
	api_confirm_order_service_view,
	api_pay_Money_view,
	api_subscription_view,
	ordersListAPIView,
	api_subscription_detail_webhook,
	api_customer_portal_view,
	api_renew_service_view
)

app_name = 'Checkout'

urlpatterns = [
	path('api/pawn', api_pawn_Money_view, name="pawnMoney"),
	path('api/renew', api_renew_service_view, name="pawnMoney"),
	path('api/subscribe', api_subscription_view, name="subscribe"),
	path('api/order', api_order_service_view, name="orderService"),

	
	path('api/confirm', api_confirm_order_service_view, name="confirmedOrderService"),
	path('api/canceled', api_canceled_order_service_view, name="canceledOrderService"),
	path('api/pay', api_pay_Money_view, name="payOwnerService"),
	path('api/orderDetail/<pk>', api_detail_order_view, name="orderDetail"),
	path('api/purchaseOrders', api_purchase_orders_view.as_view(), name="purchaseOrders"),
	path('api/requestedOrders', api_requested_orders_view.as_view(), name="requestedOrders"),
#	path('api/allOrder', ordersListAPIView.as_view(), name="allOrder"),
	path('webhook', api_subscription_detail_webhook, name="webhook"),
	path('api/customerPortal', api_customer_portal_view, name="customer portal"),

]