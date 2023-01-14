from chat.consumers import get_or_create_personal_thread
from chat.models import Message, Thread
from datetime import timedelta
from knox_allauth.models import CustomUser
from Service.models import ServicePost
from Neetechs.settings import STRIPE_WEBHOOK_SECRET
import json
from rest_framework.generics import ListAPIView
from Checkout.models import ServiceOrder
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from django.conf import settings

#from Service.models import ServicePost
from .serializers import ServiceOrderSerializer
from chat.serializers import MessageSerializers
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from knox.auth import TokenAuthentication

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# OrderService
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_order_service_view(request):
    if request.method == 'POST':
        data = request.data
        #_mutable = data._mutable
        #data._mutable = True

        #data.get('status', 1) 
        #ServiceOrder.StatusOptions
        #print(data['status'])
        serializer = ServiceOrderSerializer(data=data)
        
        #data._mutable = _mutable
        #print(data.get('status', 2))
        if serializer.is_valid() and data['customerIdd'] == request.user.site_id and data['status'] == "requested":
            orderSerializer = serializer.save()
            thread_obj = get_or_create_personal_thread(data['customerIdd'],data['employedIdd'])
            threadid = Thread.objects.get(ThreadName=thread_obj.ThreadName)
            userid = CustomUser.objects.get(site_id=data['customerIdd'])
            Message.objects.create(thread=threadid,sender=userid,text=data['message'],orderId=orderSerializer.pk,type="requested")
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def api_confirm_order_service_view(request):
    if request.method == 'PATCH':
        data = request.data
        instance = get_object(request.data['orderId'])
        messageInstance = get_message(request.data['messageId'])

        serializer = ServiceOrderSerializer(instance,data=data, partial=True)
        messageSerializer = MessageSerializers(messageInstance,data=data, partial=True)
        if data['customerIdd'] == request.user.site_id:
            _mutable = request.data._mutable
            request.data._mutable = True
            data['status'] = 'confirmed'
            data['type'] = 'confirmed'
            request.data._mutable = _mutable
            if serializer.is_valid():
                serializer.save()
                if messageSerializer.is_valid():
                    messageSerializer.save()
                    return Response(data=data)
                return Response(messageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def api_canceled_order_service_view(request):
    if request.method == 'PATCH':
        data = request.data
        instance = get_object(request.data['orderId'])
        messageInstance = get_message(request.data['messageId'])

        serializer = ServiceOrderSerializer(instance,data=data, partial=True)
        messageSerializer = MessageSerializers(messageInstance,data=data, partial=True)
        if data['customerIdd'] == request.user.site_id:
            _mutable = request.data._mutable
            request.data._mutable = True
            data['status'] = 'canceled'
            data['type'] = 'canceled'
            request.data._mutable = _mutable
            if serializer.is_valid():
                serializer.save()
                if messageSerializer.is_valid():
                    messageSerializer.save()
                    return Response(data=data)
                return Response(messageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
def get_object(pk):
    try:
        return ServiceOrder.objects.get(pk=pk)
    except ServiceOrder.DoesNotExist as e:
        return Response( {"error":"Given Order was not found."},status=404)
def get_message(pk):
    try:
        return Message.objects.get(pk=pk)
    except Message.DoesNotExist as e:
        return Response( {"error":"Given Order was not found."},status=404)
# pawnMoney

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_pawn_Money_view(request):
    if request.method == 'POST':
        try:
            data = request.data
            #data['employee'] = request.user.pk
            #data['id'] = request.user.pk
            # checkout
            #service_post = ServiceOrder.objects.get(id=data['id'])
            data['title'] = "Title:" + data['title'] + ",Service id: " + data['pk']
            #print(data)
            checkout_session = stripe.checkout.Session.create(
                mode='payment',
                success_url= 'https://www.neetechs.com/CheckoutSuccess',
                cancel_url= 'https://www.neetechs.com/CheckoutUnsuccess',
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'sek',
                            'unit_amount': data['pris'],
                            'product_data': {
                                'name': data['title'],
                               # 'id': data['stripeId'],
                               # 'images': data['image'],
                            },
                        },
                        'quantity': 1,
                    },
                ],

            )
            #print(checkout_session)
            return Response({checkout_session.id})
            #return Response(data=data)
        except ServiceOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# pawnMoney
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_renew_service_view(request):
    if request.method == 'POST':
        try:
            data = request.data
            #data['employee'] = request.user.pk
            #data['id'] = request.user.pk
            # checkout
            #service_post = ServiceOrder.objects.get(id=data['id'])
           # data['title'] = "Title:" + data['title'] + ",Service id: " + data['pk']
          #  print(data)
            checkout_session = stripe.checkout.Session.create(
                customer= request.user.stripeCustomerId,
               # customer_email= request.user.email,
                mode='payment',
                success_url= 'https://www.neetechs.com/viewservice/'+data['slug'],
                cancel_url= 'https://www.neetechs.com/CheckoutUnsuccess',
                payment_method_types=['card'],
                line_items=[
                        {
                            'price': "price_1J0BwfIR19rXEZpRXxq2n3oM",
                            'quantity': 1,
                            # 
                        },
                    ],
            )
            return Response({checkout_session.id})
            #return Response(data=data)
        except ServiceOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Portal customer page
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_customer_portal_view(request):
    if request.method == 'GET':
        try:
           # print(request.user.stripeCustomerId)
            session = stripe.billing_portal.Session.create(
                customer=request.user.stripeCustomerId,
                return_url='https://www.neetechs.com/',
            )
            return Response({session.url})
        except ServiceOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# subscription view
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_subscription_view(request):
    if request.method == 'POST':
        try:
            data = request.data
            if data['type'] != "groundplan":
                #data['employee'] = request.user.pk
                #data['id'] = request.user.pk
                # checkout
                #service_post = ServiceOrder.objects.get(id=data['id'])
                #data['title'] = "Title:" + data['title'] + ",Service id: " + data['pk']
              #  print(data)
                print(request.user.stripeCustomerId)
                checkout_session = stripe.checkout.Session.create(
                        customer= request.user.stripeCustomerId,
                       # customer_email= request.user.email,
                        mode='subscription',
                        success_url= 'https://www.neetechs.com/CheckoutSuccess',
                        cancel_url= 'https://www.neetechs.com/CheckoutUnsuccess',
                        payment_method_types=['card'],
                        line_items=[
                            {
                                'price': data['priceId'],
                                'quantity': 1,
                               # 
                            },
                        ],
                    )
                if data['type'] == 'groundplan':
                    pass
                elif data['type'] == 'premiumplanmonthly':
                    pass
                elif data['type'] == 'premiumplanmonthly':
                    pass
                print(checkout_session)
                return Response({checkout_session.id})
            #return Response(data=data)
            else:
                print(data['type'])
                return Response({data['type']})
        except ServiceOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
# subscription detail           
@api_view(['POST'])
@permission_classes((AllowAny,))
def api_subscription_detail_webhook(request):
    request_data = request.data

    if STRIPE_WEBHOOK_SECRET:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=STRIPE_WEBHOOK_SECRET)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']
    #print(data)

    if event_type == 'invoice.paid':
    # Payment is successful and the subscription is created.
    # You should provision the subscription and save the customer ID to your database.
        #print(data_object['object']customer)
        pass
       # print(data)
    elif event_type == 'checkout.session.completed':
    # Continue to provision the subscription as payments continue to be made.
    # Store the status in your database and check when a user accesses your service.
    # This approach helps you avoid hitting rate limits.
        #print(data_object['object']customer)
        #print(data_object['object']customer)
        if data_object['amount_total'] == 1500:
            #increase product date success_url
            slug = data_object['success_url'].split("/")[-1]
            service_post = ServicePost.objects.get(slug=slug)
            #print("jihad")
            #print(timedelta(days=15))
            print(service_post.expiration_date)
           # print(data_object['success_url'].split("/")[-1])
            service_post.expiration_date +=  timedelta(days=15)
            print(service_post.expiration_date)
            service_post.save()
        elif data_object['amount_total'] == 4900:
            customer = CustomUser.objects.get(stripeCustomerId=data_object['customer'])
            print(customer.subscriptionType)
            customer.subscriptionType = 'premiumplanmonthly'
            print(customer.subscriptionType)
            customer.save(update_fields=['subscriptionType'])

            # change subscriptiontype
        elif data_object['amount_total'] == 49900:
            # change subscriptiontype
            customer = CustomUser.objects.get(stripeCustomerId=data_object['customer'])
            customer.subscriptionType = 'premiumplanyearly'
            customer.save(update_fields=['subscriptionType'])
            #print(data)

        print(data)
    elif event_type == 'invoice.payment_failed':
    # The payment failed or the customer does not have a valid payment method.
    # The subscription becomes past_due. Notify your customer and send them to the
    # customer portal to update their payment information.
        pass  
     # print(data)
      #print(data)
    else:
        print('Unhandled event type {}'.format(event_type))

    return Response(data)
    #return jsonify({'status': 'success'})
# payMoney
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_pay_Money_view(request):
    if request.method == 'POST':
        try:

            # curl https://api.stripe.com/v1/balance \-u sk_test_51IwTvvIR19rXEZpRwwwDByofI7ZaWyPsGUW5hGIWKxdtD3Mg2ZAmM9xBvZ1kptffFUQSX0Lp6rW9US3EIz37A9tl00HcDB0vJz:
            # get the money
            # send it to employedIdd
            # Set your secret key. Remember to switch to your live secret key in production.
     
            data = request.data
            #data['employee'] = request.user.pk
            #data['id'] = request.user.pk
            # checkout
            #service_post = ServicePost.objects.get(id=data['id'])
            data['title'] = "Title:" + data['title'] + ",Service id: " + data['pk']
            #print(data)
            payout = stripe.Payout.create(
                amount=1000,
                currency='sek',
                method='instant',
                destination='card_xyz',
            )
           # print(payout)
            return Response({payout.id})
            #return Response(data=data)
        except ServiceOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    # pay the owner of service
@api_view(['GET', ])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_detail_order_view(request, pk):
	try:
		order = ServiceOrder.objects.get(pk=pk)
	except ServiceOrder.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	serializer = ServiceOrderSerializer(order)
	return Response(serializer.data)

class api_purchase_orders_view(ListAPIView):
    def get_queryset(self):
        return  ServiceOrder.objects.filter(employedIdd=self.request.user.site_id).order_by("-pk")
    serializer_class = ServiceOrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    OrderingFilter = ('pk','title','status')
    filterset_fields =  ['status']

class api_requested_orders_view(ListAPIView):
    def get_queryset(self):
        return  ServiceOrder.objects.filter(customerIdd=self.request.user.site_id).order_by("-pk")
    serializer_class = ServiceOrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    OrderingFilter = ('pk','title','status')

class ordersListAPIView(ListAPIView):
    queryset = ServiceOrder.objects.all().order_by("-pk")
    serializer_class = ServiceOrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    OrderingFilter = ('pk','title','status')
    filterset_fields =  ['status']
    #search_fields = ['title', 'site_id', 'beskrivning','slug', 'city','state','country','underCategory','Category','beskrivning',]

######################################################################
#### did you did the job
##### check if not return the money to buyer
##### check if yes continu
###### checl if buyer say yes he did 

#### did you ricive your product

#### if not 


###### contakt support