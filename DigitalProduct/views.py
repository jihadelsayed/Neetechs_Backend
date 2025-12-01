import boto3
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import DigitalProduct, DigitalProductPurchase
from .serializers import (
    DigitalProductListSerializer,
    DigitalProductDetailSerializer,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def digital_product_list(request):
    qs = DigitalProduct.objects.filter(is_active=True)
    serializer = DigitalProductListSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([AllowAny])
def digital_product_detail(request, slug):
    try:
        product = DigitalProduct.objects.get(slug=slug, is_active=True)
    except DigitalProduct.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = DigitalProductDetailSerializer(product, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_digital_product(request, product_id):
    # Check ownership
    try:
        product = DigitalProduct.objects.get(id=product_id, is_active=True)
    except DigitalProduct.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if not DigitalProductPurchase.objects.filter(
        user=request.user, product=product
    ).exists():
        return Response(
            {"detail": "You don't own this product."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if not product.file:
        return Response(
            {"detail": "File not available."},
            status=status.HTTP_404_NOT_FOUND,
        )

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.AWS_PRODUCTS_BUCKET_NAME,
            "Key": product.file.name,
        },
        ExpiresIn=3600,  # 1 hour
    )

    return Response({"download_url": url})
