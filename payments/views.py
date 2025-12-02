# payments/views.py

import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from knox_allauth.models import CustomUser  # adjust if your user model is elsewhere
from DigitalProduct.models import (
    DigitalProduct,
    DigitalProductPurchase,
    DigitalProductBundle,
    DigitalProductBundlePurchase,
)
 
stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook endpoint:
    - Handles checkout.session.completed for single products or bundles
    - Uses metadata: user_id (optional), digital_product_id, bundle_id
    - For guests: attaches/creates a user from the Stripe email.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {}) or {}

        user_id = metadata.get("user_id")
        product_id = metadata.get("digital_product_id")
        bundle_id = metadata.get("bundle_id")

        user = None

        # 1) Logged-in user passed from frontend
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                user = None

        # 2) Guest checkout → try to attach/create user by email
        if not user:
            customer_details = session.get("customer_details") or {}
            email = customer_details.get("email")
            if email:
                user, _ = CustomUser.objects.get_or_create(
                    email=email,
                    defaults={"username": email},
                )

        if not user:
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
@permission_classes([AllowAny])
def create_checkout_session(request):
    """
    Create Stripe Checkout session for a single digital product.
    Expects: { "product_id": <int> }
    Works for both logged-in and guest users.
    Uses local price + inline product_data (no stored Stripe product id needed).
    """
    product_id = request.data.get("product_id")

    if not product_id:
        return Response({"detail": "product_id required"}, status=400)

    try:
        product = DigitalProduct.objects.get(id=product_id, is_active=True)
    except DigitalProduct.DoesNotExist:
        return Response({"detail": "Product not found"}, status=404)

    if product.price is None:
        return Response(
            {"detail": "Product missing local price value"}, status=500
        )

    user = request.user if request.user.is_authenticated else None

    metadata = {"digital_product_id": str(product.id)}
    if user:
        metadata["user_id"] = str(user.id)

    amount_cents = int(product.price * 100)

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",          # change if not USD
                    "unit_amount": amount_cents,
                    "product_data": {
                        "name": product.title,
                        "description": product.short_description,
                        "metadata": {
                            "digital_product_id": str(product.id),
                        },
                    },
                },
                "quantity": 1,
            }
        ],
        success_url=f"{settings.FRONTEND_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=settings.FRONTEND_CANCEL_URL,
        metadata=metadata,
    )

    return Response({"checkout_url": session.url})


@api_view(["POST"])
@permission_classes([AllowAny])
def create_bundle_checkout_session(request):
    """
    Create Stripe Checkout session for a bundle.
    Expects: { "bundle_id": <int> }
    Works for both logged-in and guest users.
    Uses local price + inline product_data (no stored Stripe product id needed).
    """
    bundle_id = request.data.get("bundle_id")

    if not bundle_id:
        return Response({"detail": "bundle_id required"}, status=400)

    try:
        bundle = DigitalProductBundle.objects.get(id=bundle_id, is_active=True)
    except DigitalProductBundle.DoesNotExist:
        return Response({"detail": "Bundle not found"}, status=404)

    if bundle.price is None:
        return Response(
            {"detail": "Bundle missing local price value"}, status=500
        )

    user = request.user if request.user.is_authenticated else None

    metadata = {"bundle_id": str(bundle.id)}
    if user:
        metadata["user_id"] = str(user.id)

    amount_cents = int(bundle.price * 100)

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": amount_cents,
                    "product_data": {
                        "name": bundle.title,
                        "description": bundle.short_description,
                        "metadata": {
                            "bundle_id": str(bundle.id),
                        },
                    },
                },
                "quantity": 1,
            }
        ],
        success_url=f"{settings.FRONTEND_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=settings.FRONTEND_CANCEL_URL,
        metadata=metadata,
    )

    return Response({"checkout_url": session.url})

@api_view(["GET"])
@permission_classes([AllowAny])
def checkout_session_detail(request, session_id):
    """
    Public endpoint:
    - Frontend sends session_id from Stripe redirect (?session_id=...)
    - We call Stripe to verify and return minimal info for Angular
    """
    try:
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=["line_items"]
        )
    except stripe.error.InvalidRequestError:
        return Response({"detail": "Invalid session id"}, status=400)

    metadata = session.get("metadata", {}) or {}

    product_name = None
    product_slug = None
    download_url = None

    product_id = metadata.get("digital_product_id")
    bundle_id = metadata.get("bundle_id")

    # Single digital product
    if product_id:
        try:
            product = DigitalProduct.objects.get(id=product_id)
            product_name = product.title
            product_slug = product.slug
            # عدّل هذا حسب اسم حقل الرابط عندك في الموديل (مثلاً download_url أو file.url إلخ)
            download_url = getattr(product, "download_url", None)
        except DigitalProduct.DoesNotExist:
            pass

    # Bundle
    elif bundle_id:
        try:
            bundle = DigitalProductBundle.objects.get(id=bundle_id)
            product_name = bundle.title
            product_slug = bundle.slug
            download_url = getattr(bundle, "download_url", None)
        except DigitalProductBundle.DoesNotExist:
            pass

    data = {
        "id": session.id,
        "status": session.payment_status,  # "paid", "unpaid", etc.
        "product_name": product_name,
        "product_slug": product_slug,
        "download_url": download_url,
        "amount_total": session.get("amount_total"),
        "currency": session.get("currency"),
    }
    return Response(data)