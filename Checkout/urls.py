"""URL patterns for the Checkout app, defining routes for order management,
payments, and Stripe integration.
"""
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

app_name = 'Checkout' # Defines the application namespace for these URLs.

urlpatterns = [ # List of URL patterns for the checkout and payment process.
	# Handles creation of Stripe one-time payment sessions (potentially for "pawning" a service).
	path('pawn', api_pawn_Money_view, name="pawnMoney"),
	# Handles creation of Stripe payment sessions for service renewal.
	# Note: URL name "pawnMoney" is duplicated, consider renaming for clarity (e.g., "renewServicePayment").
	path('renew', api_renew_service_view, name="pawnMoney"),
	# Handles creation of Stripe subscription sessions.
	path('subscribe', api_subscription_view, name="subscribe"),
	# Handles the creation of a new service order.
	path('order', api_order_service_view, name="orderService"),

	
	# Handles confirmation of an existing service order.
	path('confirm', api_confirm_order_service_view, name="confirmedOrderService"),
	# Handles cancellation of an existing service order.
	path('canceled', api_canceled_order_service_view, name="canceledOrderService"),
	# Handles payout creation (conceptual, needs proper destination).
	path('pay', api_pay_Money_view, name="payOwnerService"),
	# Retrieves details of a specific service order.
	path('orderDetail/<pk>', api_detail_order_view, name="orderDetail"),
	# Lists service orders where the authenticated user is the employee/provider.
	path('purchaseOrders', api_purchase_orders_view.as_view(), name="purchaseOrders"),
	# Lists service orders requested by the authenticated user.
	path('requestedOrders', api_requested_orders_view.as_view(), name="requestedOrders"),
	# TODO: This path is commented out. Review if `ordersListAPIView` is needed and either implement or remove this line.
#	path('allOrder', ordersListAPIView.as_view(), name="allOrder"),
	# Stripe webhook endpoint for handling subscription and payment events.
	path('webhook', api_subscription_detail_webhook, name="webhook"),
	# Provides access to the Stripe customer billing portal.
	path('customerPortal', api_customer_portal_view, name="customer portal"), # Consider renaming to "customerPortal" for consistency.

]