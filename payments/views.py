# payments/views.py

import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from knox_allauth.models import CustomUser  # adjust if your user model is elsewhere
from DigitalProduct.models import (
    DigitalProduct,
    DigitalProductPurchase,
    DigitalProductBundle,
    DigitalProductBundlePurchase,
)

# Stripe secret key from your .env
stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook endpoint:
    - checkout.session.completed for single products or bundles
    - uses metadata: user_id, digital_product_id, bundle_id
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # set in .env

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret,
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {}) or {}

        user_id = metadata.get("user_id")
        product_id = metadata.get("digital_product_id")
        bundle_id = metadata.get("bundle_id")

        if not user_id:
            return HttpResponse(status=200)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return HttpResponse(status=200)

        # Single product purchase
        if product_id:
            try:
                product = DigitalProduct.objects.get(id=product_id)
            except DigitalProduct.DoesNotExist:
                return HttpResponse(status=200)

            DigitalProductPurchase.objects.update_or_create(
                user=user,
                product=product,
                defaults={
                    "version": product.version,
                    "stripe_payment_intent": session.get("payment_intent", ""),
                },
            )

        # Bundle purchase
        elif bundle_id:
            try:
                bundle = DigitalProductBundle.objects.get(id=bundle_id)
            except DigitalProductBundle.DoesNotExist:
                return HttpResponse(status=200)

            DigitalProductBundlePurchase.objects.update_or_create(
                user=user,
                bundle=bundle,
                defaults={
                    "stripe_payment_intent": session.get("payment_intent", ""),
                },
            )

    return HttpResponse(status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    """
    Create Stripe Checkout session for a single digital product.
    Expects: { "product_id": <int> }
    """
    product_id = request.data.get("product_id")

    if not product_id:
        return Response({"detail": "product_id required"}, status=400)

    try:
        product = DigitalProduct.objects.get(id=product_id, is_active=True)
    except DigitalProduct.DoesNotExist:
        return Response({"detail": "Product not found"}, status=404)

    if not product.stripe_price_id:
        return Response(
            {"detail": "Product missing Stripe price ID"}, status=500
        )

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price": product.stripe_price_id,
                "quantity": 1,
            }
        ],
        success_url=settings.FRONTEND_SUCCESS_URL,
        cancel_url=settings.FRONTEND_CANCEL_URL,
        metadata={
            "user_id": request.user.id,
            "digital_product_id": str(product.id),
        },
    )

    return Response({"checkout_url": session.url})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_bundle_checkout_session(request):
    """
    Create Stripe Checkout session for a bundle.
    Expects: { "bundle_id": <int> }
    """
    bundle_id = request.data.get("bundle_id")

    if not bundle_id:
        return Response({"detail": "bundle_id required"}, status=400)

    try:
        bundle = DigitalProductBundle.objects.get(id=bundle_id, is_active=True)
    except DigitalProductBundle.DoesNotExist:
        return Response({"detail": "Bundle not found"}, status=404)

    if not bundle.stripe_price_id:
        return Response(
            {"detail": "Bundle missing Stripe price ID"}, status=500
        )

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price": bundle.stripe_price_id,
                "quantity": 1,
            }
        ],
        success_url=settings.FRONTEND_SUCCESS_URL,
        cancel_url=settings.FRONTEND_CANCEL_URL,
        metadata={
            "user_id": request.user.id,
            "bundle_id": str(bundle.id),
        },
    )

    return Response({"checkout_url": session.url})
