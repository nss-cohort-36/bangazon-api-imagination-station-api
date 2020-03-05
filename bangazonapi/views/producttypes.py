"""product_types for bangazon"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import ProductType
from .products import ProductsSerializer


class ProductTypesSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product_types

    Arguments:
        serializers
    """
    products = ProductsSerializer(many=True)
    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='product_type',
            lookup_field='id'
        )

        # products referst to the related_name attribute in products.py
        fields = ('id', 'url', 'name', 'products')
        depth = 2


class ProductTypes(ViewSet):
    """product_types for bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ProductType instance
        """
        new_product_type = ProductType()
        new_product_type.name = request.data["name"]

        new_product_type.save()

        serializer = ProductTypesSerializer(
            new_product_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product_type

        Returns:
            Response -- JSON serialized product_type instance
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypesSerializer(
                product_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a product_type

        Returns:
            Response -- Empty body with 204 status code
        """
        product_type = ProductType.objects.get(pk=pk)
        product_type.name = request.data["name"]

        product_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product_type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            product_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to product_types resource

        Returns:
            Response -- JSON serialized list of product_types
        """
        product_types = ProductType.objects.all()

        serializer = ProductTypesSerializer(
            product_types, many=True, context={'request': request})
        return Response(serializer.data)
