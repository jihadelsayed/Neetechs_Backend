"""
Defines views for handling service orders, payments, Stripe integration,
and related checkout processes within the Neetechs platform.
"""
from chat.consumers import get_or_create_personal_thread
from chat.models import Message, Thread
from datetime import timedelta
from accounts.models import User
from Service.models import ServicePost
from Neetechs.settings import STRIPE_WEBHOOK_SECRET
from Neetechs.permissions import ReadOnlyOrStaff, StripeWebhookPermission
import json
from rest_framework.generics import ListAPIView
from Checkout.models import ServiceOrder
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.conf import settings

#from Service.models import ServicePost
from .serializers import ServiceOrderSerializer
from chat.serializers import MessageSerializer
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from knox.auth import TokenAuthentication

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes

# OrderService
@extend_schema(request=None, 
               tags=["order-service"],
               responses={200: OpenApiResponse(OpenApiTypes.OBJECT)})
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_order_service_view(request):
    """
    Handles the creation of a new service order.

    Method: POST
    Permissions: IsAuthenticated
    Request Data:
        - customerIdd (str): Site ID of the customer.
        - employedIdd (str): Site ID of the employee/provider.
        - message (str): Initial message related to the order.
        - status (str, optional): Initial status, defaults to "requested".
        - Other fields required by ServiceOrderSerializer.
    Logic:
        - Validates that the requesting user is the customer.
        - Validates that the initial status is "requested".
        - Saves the ServiceOrder instance.
        - Creates or retrieves a personal chat thread between customer and employee.
        - Creates a new message in the thread associated with the order.
    Response:
        - Success: Returns the original request data (consider returning serialized order).
        - Error: Returns serializer errors with HTTP 400.
    """
    if request.method == 'POST':
        data = request.data
        # Note: Mutability of request.data is handled carefully below if needed,
        # but directly using data for serializer should be fine for creation.
        serializer = ServiceOrderSerializer(data=data)
        
        # Validate that the authenticated user is the one placing the order
        # and that the order status is "requested" upon creation.
        if serializer.is_valid() and data['customerIdd'] == request.user.site_id and data['status'] == "requested":
            orderSerializer = serializer.save() # Save the service order.
            # Get or create a chat thread for this order.
            thread_obj = get_or_create_personal_thread(data['customerIdd'],data['employedIdd'])
            threadid = Thread.objects.get(ThreadName=thread_obj.ThreadName)
            userid = User.objects.get(site_id=data['customerIdd'])
            # Create an initial message related to the service request.
            Message.objects.create(thread=threadid,sender=userid,text=data['message'],orderId=orderSerializer.pk,type="requested")
            return Response(data=data) # Consider returning a more specific success response or serialized data.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=None,
               
               tags=["order-service"],
               responses={200: OpenApiResponse(OpenApiTypes.OBJECT)})
@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def api_confirm_order_service_view(request):
    """
    Confirms an existing service order.

    Method: PATCH
    Permissions: IsAuthenticated
    Request Data:
        - orderId (int): Primary key of the ServiceOrder to confirm.
        - messageId (int): Primary key of the Message associated with the confirmation.
        - customerIdd (str): Site ID of the customer (for validation).
        - Other fields to update on ServiceOrder or Message.
    Logic:
        - Retrieves the ServiceOrder and Message instances.
        - Validates that the requesting user is the customer.
        - Updates the status of the ServiceOrder to "confirmed".
        - Updates the type of the Message to "confirmed".
    Response:
        - Success: Returns the modified request data.
        - Error: Returns serializer errors or HTTP 400/404.
    """
    if request.method == 'PATCH':
        data = request.data
        instance = get_object(request.data['orderId']) # Retrieve the ServiceOrder.
        if isinstance(instance, Response): # Check if get_object returned an error Response
            return instance
        messageInstance = get_message(request.data['messageId']) # Retrieve the Message.
        if isinstance(messageInstance, Response): # Check if get_message returned an error Response
            return messageInstance

        serializer = ServiceOrderSerializer(instance,data=data, partial=True)
        messageSerializer = MessageSerializer(messageInstance,data=data, partial=True)
        
        # Validate that the authenticated user is the customer associated with the order.
        if data['customerIdd'] == request.user.site_id:
            # Make a mutable copy of request.data to modify 'status' and 'type'.
            # Direct modification of request.data is generally discouraged.
            modified_data = data.copy()
            modified_data['status'] = 'confirmed'
            modified_data['type'] = 'confirmed'
            
            # Re-initialize serializers with the modified data for update
            serializer = ServiceOrderSerializer(instance, data=modified_data, partial=True)
            messageSerializer = MessageSerializer(messageInstance, data=modified_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                if messageSerializer.is_valid():
                    messageSerializer.save()
                    return Response(data=modified_data) # Return modified data on success.
                return Response(messageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "User not authorized to confirm this order."}, status=status.HTTP_403_FORBIDDEN)

@extend_schema(request=None,
               tags=["order-service"],
               responses={200: OpenApiResponse(OpenApiTypes.OBJECT)})
@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def api_canceled_order_service_view(request):
    """
    Cancels an existing service order.

    Method: PATCH
    Permissions: IsAuthenticated
    Request Data:
        - orderId (int): Primary key of the ServiceOrder to cancel.
        - messageId (int): Primary key of the Message associated with the cancellation.
        - customerIdd (str): Site ID of the customer (for validation).
        - Other fields to update.
    Logic:
        - Retrieves ServiceOrder and Message instances.
        - Validates that the requesting user is the customer.
        - Updates ServiceOrder status to "canceled".
        - Updates Message type to "canceled".
    Response:
        - Success: Returns the modified request data.
        - Error: Returns serializer errors or HTTP 400/403/404.
    """
    if request.method == 'PATCH':
        data = request.data
        instance = get_object(request.data['orderId']) # Retrieve the ServiceOrder.
        if isinstance(instance, Response): return instance # Propagate error if any
        messageInstance = get_message(request.data['messageId']) # Retrieve the Message.
        if isinstance(messageInstance, Response): return messageInstance # Propagate error

        serializer = ServiceOrderSerializer(instance,data=data, partial=True)
        messageSerializer = MessageSerializer(messageInstance,data=data, partial=True)

        if data['customerIdd'] == request.user.site_id:
            modified_data = data.copy()
            modified_data['status'] = 'canceled'
            modified_data['type'] = 'canceled'

            serializer = ServiceOrderSerializer(instance, data=modified_data, partial=True)
            messageSerializer = MessageSerializer(messageInstance, data=modified_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                if messageSerializer.is_valid():
                    messageSerializer.save()
                    return Response(data=modified_data)
                return Response(messageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "User not authorized to cancel this order."}, status=status.HTTP_403_FORBIDDEN)

def get_object(pk):
    """
    Retrieves a ServiceOrder instance by its primary key.

    Args:
        pk (int): The primary key of the ServiceOrder.

    Returns:
        ServiceOrder: The retrieved ServiceOrder instance.
        Response: An HTTP 404 Response if the ServiceOrder is not found.
    """
    try:
        return ServiceOrder.objects.get(pk=pk)
    except ServiceOrder.DoesNotExist:
        return Response( {"error":"Given Order was not found."},status=status.HTTP_404_NOT_FOUND)

def get_message(pk):
    """
    Retrieves a Message instance by its primary key.

    Args:
        pk (int): The primary key of the Message.

    Returns:
        Message: The retrieved Message instance.
        Response: An HTTP 404 Response if the Message is not found.
    """
    try:
        return Message.objects.get(pk=pk)
    except Message.DoesNotExist: # Corrected exception type
        return Response( {"error":"Given Message was not found."},status=status.HTTP_404_NOT_FOUND)

# pawnMoney - This term might be domain-specific, referring to a type of payment.
@extend_schema(request=None,
               
                tags=["order-service"],
               responses={200: OpenApiResponse(OpenApiTypes.OBJECT)})
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_pawn_Money_view(request):
    """
    Creates a Stripe Checkout Session for a one-time payment (potentially for "pawning" a service).

    Method: POST
    Permissions: IsAuthenticated
    Request Data:
        - title (str): Title of the service/item.
        - pk (str): Primary key or identifier for the service.
        - pris (int): Price of the service in the smallest currency unit (e.g., öre for SEK).
    Logic:
        - Constructs a title for the Stripe product.
        - Calls Stripe API to create a Checkout Session.
    Response:
        - Success: Returns the Stripe Checkout Session ID.
        - Error: HTTP 404 if ServiceOrder.DoesNotExist (though ServiceOrder is not directly fetched here, this might be legacy).
    """
    if request.method == 'POST':
        try:
            data = request.data
            # The title is constructed for display on the Stripe checkout page.
            display_title = "Title:" + data.get('title', 'Service') + ",Service id: " + str(data.get('pk', 'N/A'))
            
            # Creates a Stripe Checkout session for one-time payment.
            checkout_session = stripe.checkout.Session.create(
                mode='payment',
                success_url= 'https://www.neetechs.com/CheckoutSuccess', # URL for successful payment.
                cancel_url= 'https://www.neetechs.com/CheckoutUnsuccess',   # URL for canceled payment.
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'sek', # Currency for the payment.
                            'unit_amount': data['pris'], # Price in smallest currency unit.
                            'product_data': {
                                'name': display_title, # Name of the product/service.
                            },
                        },
                        'quantity': 1,
                    },
                ],
            )
            return Response({checkout_session.id})
        except ServiceOrder.DoesNotExist: # This exception might not be relevant here as ServiceOrder isn't fetched.
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e: # Generic exception handler for Stripe API errors or other issues.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(request=None, 
               tags=["order-service"],
               responses={200: OpenApiResponse(OpenApiTypes.OBJECT)})
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_renew_service_view(request):
    """
    Creates a Stripe Checkout Session for renewing a service, likely with a fixed price.

    Method: POST
    Permissions: IsAuthenticated
    Request Data:
        - slug (str): Slug of the service to be renewed (used in success_url).
        - Potentially other data, though not explicitly used for Stripe session creation logic shown.
    Logic:
        - Uses the authenticated user's `stripeCustomerId`.
        - Creates a Stripe Checkout Session with a predefined price ID ("price_1J0BwfIR19rXEZpRXxq2n3oM").
    Response:
        - Success: Returns the Stripe Checkout Session ID.
        - Error: HTTP 404 if ServiceOrder.DoesNotExist (legacy exception handling).
                 HTTP 500 for other errors.
    """
    if request.method == 'POST':
        try:
            data = request.data
            # Creates a Stripe Checkout session for a specific, possibly fixed-price, service renewal.
            checkout_session = stripe.checkout.Session.create(
                customer= request.user.stripeCustomerId, # Associates the session with an existing Stripe customer.
                mode='payment',
                success_url= 'https://www.neetechs.com/viewservice/'+data['slug'], # Redirect URL after successful renewal.
                cancel_url= 'https://www.neetechs.com/CheckoutUnsuccess',
                payment_method_types=['card'],
                line_items=[
                        {
                            'price': "price_1J0BwfIR19rXEZpRXxq2n3oM", # Predefined Stripe Price ID for the renewal.
                            'quantity': 1,
                        },
                    ],
            )
            return Response({checkout_session.id})
        except ServiceOrder.DoesNotExist: # Legacy, may not be directly applicable.
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(request=None,                tags=["order-service"],
responses={200: OpenApiResponse(OpenApiTypes.OBJECT)})
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_customer_portal_view(request):
    """
    Creates and returns a URL for the Stripe Customer Billing Portal.

    Method: GET
    Permissions: IsAuthenticated
    Logic:
        - Retrieves the Stripe Customer ID for the authenticated user.
        - Calls Stripe API to create a Billing Portal Session.
    Response:
        - Success: Returns the URL to the Stripe Customer Portal.
        - Error: HTTP 404 if ServiceOrder.DoesNotExist (legacy).
                 HTTP 500 for Stripe API errors.
    """
    if request.method == 'GET':
        try:
            # Creates a Stripe Billing Portal session for the authenticated user.
            session = stripe.billing_portal.Session.create(
                customer=request.user.stripeCustomerId, # Stripe Customer ID of the user.
                return_url='https://www.neetechs.com/', # URL to return to after leaving the portal.
            )
            return Response({session.url})
        except ServiceOrder.DoesNotExist: # Legacy, may not be directly applicable.
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(request=None,                tags=["order-service"],
responses={200: OpenApiResponse(OpenApiTypes.OBJECT)})
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_subscription_view(request):
    """
    Handles creation of a Stripe Checkout Session for a subscription.

    Method: POST
    Permissions: IsAuthenticated
    Request Data:
        - type (str): Type of subscription (e.g., "premiumplanmonthly"). If "groundplan", no Stripe session is created.
        - priceId (str): Stripe Price ID for the subscription plan.
    Logic:
        - If type is not "groundplan", creates a Stripe Checkout Session in 'subscription' mode.
        - Uses the authenticated user's `stripeCustomerId`.
    Response:
        - Success (for non-groundplan): Returns the Stripe Checkout Session ID.
        - Success (for groundplan): Returns the type of plan.
        - Error: HTTP 404 (legacy) or HTTP 500.
    """
    if request.method == 'POST':
        try:
            data = request.data
            if data['type'] != "groundplan":
                # Creates a Stripe Checkout Session for starting a new subscription.
                checkout_session = stripe.checkout.Session.create(
                        customer= request.user.stripeCustomerId,
                        mode='subscription',
                        success_url= 'https://www.neetechs.com/CheckoutSuccess',
                        cancel_url= 'https://www.neetechs.com/CheckoutUnsuccess',
                        payment_method_types=['card'],
                        line_items=[
                            {
                                'price': data['priceId'], # Stripe Price ID for the selected subscription.
                                'quantity': 1,
                            },
                        ],
                    )
                # The following conditional logic seems redundant as no action is taken.
                # if data['type'] == 'groundplan':
                #     pass
                # elif data['type'] == 'premiumplanmonthly':
                #     pass
                # elif data['type'] == 'premiumplanmonthly': # Duplicate condition
                #     pass
                return Response({checkout_session.id})
            else:
                # For "groundplan", no Stripe interaction is needed, just return the plan type.
                return Response({data['type']})
        except ServiceOrder.DoesNotExist: # Legacy exception.
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
@extend_schema(request=None,                tags=["order-service"],
responses={200: OpenApiResponse(OpenApiTypes.OBJECT)})
@api_view(['POST'])
# Validate Stripe signatures before processing.
@permission_classes((StripeWebhookPermission,))
def api_subscription_detail_webhook(request):
    """
    Handles incoming webhooks from Stripe for subscription and payment events.

    Method: POST
    Permissions: StripeWebhookPermission (secured by Stripe signature verification).
    Request Data: Stripe event payload.
    Logic:
        - Verifies the Stripe webhook signature.
        - Processes different event types:
            - `invoice.paid`: (Currently no specific action) Indicates a successful subscription payment.
            - `checkout.session.completed`: Handles post-payment actions like:
                - Extending service expiration date for specific one-time payments.
                - Updating user's subscription type in the local database.
            - `invoice.payment_failed`: (Currently no specific action) Indicates a failed payment.
    Response:
        - Success: Returns the event data object.
        - Error: Returns an error response if signature verification fails or an exception occurs.
    """
    event = getattr(request, "_stripe_event", None)
    if event is None:
        if not STRIPE_WEBHOOK_SECRET:
            return Response({"error": "Missing Stripe webhook secret."}, status=status.HTTP_400_BAD_REQUEST)
        # Retrieve the event by verifying the signature using the raw body and secret (fallback when permission wasn't applied).
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.body, sig_header=signature, secret=STRIPE_WEBHOOK_SECRET)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) # Return specific error for signature issue.

    data = event['data']
    event_type = event['type']
    data_object = data['object']

    if event_type == 'invoice.paid':
        # Logic for when a subscription payment is successfully made.
        # For example, ensuring continued access to services.
        pass # Placeholder for future logic.
    elif event_type == 'checkout.session.completed':
        # Logic for when a checkout session (payment or subscription setup) is completed.
        if data_object.get('mode') == 'payment' and data_object.get('amount_total') == 1500: # Assuming 15.00 SEK for a specific service.
            # Example: Extend service duration after a specific one-time payment.
            success_url = data_object.get('success_url', '')
            if '/viewservice/' in success_url: # Check if it's a service renewal based on success URL.
                slug = success_url.split("/")[-1]
                try:
                    service_post = ServicePost.objects.get(slug=slug)
                    service_post.expiration_date +=  timedelta(days=15) # Extend by 15 days.
                    service_post.save()
                except ServicePost.DoesNotExist:
                    print(f"ServicePost with slug {slug} not found for checkout.session.completed event.")
        
        elif data_object.get('mode') == 'subscription': # Handling subscription creation/change
            # Logic for when a subscription is successfully created or changed via checkout.
            stripe_customer_id = data_object.get('customer')
            if stripe_customer_id:
                try:
                    customer = User.objects.get(stripeCustomerId=stripe_customer_id)
                    # Determine new subscription type based on amount or price ID (more robust).
                    # This example uses amount_total, which might be less reliable than price ID.
                    if data_object.get('amount_total') == 4900: # Example: 49.00 SEK for monthly premium.
                        customer.subscriptionType = 'premiumplanmonthly'
                        customer.save(update_fields=['subscriptionType'])
                    elif data_object.get('amount_total') == 49900: # Example: 499.00 SEK for yearly premium.
                        customer.subscriptionType = 'premiumplanyearly'
                        customer.save(update_fields=['subscriptionType'])
                except User.DoesNotExist:
                    print(f"User with stripeCustomerId {stripe_customer_id} not found.")

    elif event_type == 'invoice.payment_failed':
        # Logic for when a subscription payment fails.
        # For example, notify the user, restrict service access.
        pass # Placeholder for future logic. 
    else:
        print('Unhandled event type {}'.format(event_type))

    return Response(data_object) # Return the Stripe data object for acknowledgment.

@extend_schema(request=None,                tags=["order-service"],
responses={200: OpenApiResponse(OpenApiTypes.OBJECT)})
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_pay_Money_view(request):
    """
    Handles payout creation via Stripe (conceptual - destination is hardcoded).

    Method: POST
    Permissions: IsAuthenticated
    Request Data:
        - title (str): Title of the service/item.
        - pk (str): Primary key or identifier.
        - (Assumes other necessary data for payout not explicitly shown in current logic)
    Logic:
        - Constructs a title.
        - Calls Stripe API to create a Payout. **Note: `destination` is hardcoded to 'card_xyz',
          which is a placeholder and will not work in a real scenario. Real implementation
          would require valid connected account or bank account details.**
    Response:
        - Success: Returns the Stripe Payout ID.
        - Error: HTTP 404 (legacy) or HTTP 500.
    """
    if request.method == 'POST':
        try:
            data = request.data
            # Title construction for payout description (internal reference).
            payout_description = "Title:" + data.get('title', 'Service Payment') + ",Service id: " + str(data.get('pk', 'N/A'))
            
            # Creates a Stripe Payout.
            # WARNING: The 'destination' field is hardcoded and needs to be dynamically set
            # to a valid connected account ID or bank account token in a real application.
            payout = stripe.Payout.create(
                amount=1000, # Amount in smallest currency unit (e.g., 10.00 SEK).
                currency='sek',
                method='instant', # Or 'standard'. Instant payouts have specific requirements.
                destination='card_xyz', # Placeholder - THIS NEEDS TO BE A VALID DESTINATION.
                description=payout_description
            )
            return Response({payout.id})
        except ServiceOrder.DoesNotExist: # Legacy exception.
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(request=None,                tags=["order-service"],
responses={200: ServiceOrderSerializer})
@api_view(['GET', ])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_detail_order_view(request, id):
    """
    Retrieves and returns the details of a specific service order.

    Method: GET
    Permissions: IsAuthenticatedOrReadOnly (anyone can view order details if they have the PK).
    Path Parameter:
        - pk (int): Primary key of the ServiceOrder.
    Logic:
        - Fetches the ServiceOrder by its primary key.
        - Serializes the order data.
    Response:
        - Success: Returns serialized ServiceOrder data.
        - Error: HTTP 404 if the order is not found.
    """
    try:
        order = ServiceOrder.objects.get(pk=id)
    except ServiceOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ServiceOrderSerializer(order)
    return Response(serializer.data)

@extend_schema(tags=["order-service"])
class api_purchase_orders_view(ListAPIView):
    """
    Lists service orders where the authenticated user is the employee/provider.
    Orders are listed in reverse primary key order (newest first).

    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Filtering: Supports filtering by 'status' via query parameters.
               Supports searching and ordering via `SearchFilter` and `OrderingFilter`.
    """
    serializer_class = ServiceOrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter] # Enables various filtering options.
    OrderingFilter = ('pk','title','status') # Fields available for ordering.
    filterset_fields =  ['status'] # Fields available for exact match filtering.
    # search_fields are typically defined on the view, not OrderingFilter.
    # search_fields = ('some_field_on_ServiceOrder', 'another_field') # Example

    def get_queryset(self):
        """Returns orders where the current user is the employee, ordered by newest first."""
        request = getattr(self, "request", None)
        if (
            getattr(self, "swagger_fake_view", False)
            or not request
            or not getattr(request, "user", None)
            or not request.user.is_authenticated
        ):
            return ServiceOrder.objects.none()
        return ServiceOrder.objects.filter(employedIdd=request.user.site_id).order_by("-pk")
@extend_schema(tags=["order-service"])

class api_requested_orders_view(ListAPIView):
    """
    Lists service orders requested by the currently authenticated user (customer).
    Orders are listed in reverse primary key order (newest first).

    Authentication: TokenAuthentication
    Permissions: IsAuthenticated
    Ordering: Supports ordering by 'pk', 'title', 'status'. (Note: 'title' is not a direct field on ServiceOrder).
    """
    serializer_class = ServiceOrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    OrderingFilter = ('pk','title','status') # 'title' might refer to a related field or needs adjustment.
    # For explicit ordering, consider adding `ordering_fields` attribute or using `OrderingFilter` in `filter_backends`.

    def get_queryset(self):
        """Returns orders where the current user is the customer, ordered by newest first."""
        request = getattr(self, "request", None)
        if (
            getattr(self, "swagger_fake_view", False)
            or not request
            or not getattr(request, "user", None)
            or not request.user.is_authenticated
        ):
            return ServiceOrder.objects.none()
        return ServiceOrder.objects.filter(customerIdd=request.user.site_id).order_by("-pk")
@extend_schema(tags=["order-service"])

class ordersListAPIView(ListAPIView):
    """
    Lists all service orders, typically for admin or general browsing with appropriate permissions.
    Orders are listed in reverse primary key order (newest first).

    Authentication: TokenAuthentication
    Permissions: ReadOnlyOrStaff (public read access, staff-only writes).
    Filtering: Supports filtering by 'status'.
               Supports searching and ordering.
    """
    queryset = ServiceOrder.objects.all().order_by("-pk")
    serializer_class = ServiceOrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ReadOnlyOrStaff]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    OrderingFilter = ('pk','title','status') # 'title' might refer to a related field.
    filterset_fields =  ['status']
    # search_fields = ('field_to_search1', 'related_object__field_to_search2') # Example
    #search_fields = ['title', 'site_id', 'beskrivning','slug', 'city','state','country','underCategory','Category','beskrivning',]

######################################################################
#### did you did the job
##### check if not return the money to buyer
##### check if yes continu
###### checl if buyer say yes he did 

#### did you ricive your product

#### if not 


###### contakt support
