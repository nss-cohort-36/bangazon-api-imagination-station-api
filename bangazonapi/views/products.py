"""products for bangazon"""
from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from bangazonapi.models import Product
from .customers import CustomersSerializer


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    Arguments:
        serializers
    """

    customer = CustomersSerializer()

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'price', 'description',
                  'quantity', 'location', 'image_path', 'customer', 'product_type', )
        depth = 2


class Products(ViewSet):
    """products for bangazon"""

    # Custom action to get the number of products sold for specific product
    @action(methods=['get'], detail=False, url_name="num_sold")
    def num_sold(self, request):
        """Handle requests total sold of a product.

        Fetch call to get number sold for a product:
            http://localhost:8000/products/num_sold?product_id=PRODUCT_ID_GOES_HERE

        Author:
            Ryan Crowley

        Returns:
            Response - JSON object with "total" as the key and an integer as the value
        """

        # Get the product ID from the query params
        product_id = int(self.request.query_params.get('product_id'))

        # query the database
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT COUNT() as "Number Sold"
                    FROM bangazonapi_orderproduct op
                    JOIN bangazonapi_order o
                    ON op.order_id = o.id
                    WHERE op.product_id = %s
                    AND o.payment_type_id is not NULL''', [product_id]
            )

            row = cursor.fetchone()
            # row[0] will contain the integer representing total sold for this product.
            total = {"total_sold": row[0]}

            # Return a JSON response
            return Response(total)


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Product instance
        """
        new_product = Product()
        new_product.name = request.data["name"]
        new_product.price = request.data["price"]
        new_product.description = request.data["description"]
        new_product.quantity = request.data["quantity"]
        new_product.location = request.data["location"]
        new_product.image_path = request.data["image_path"]
        new_product.customer_id = request.auth.user.customer.id
        new_product.product_type_id = request.data["product_type_id"]

        new_product.save()

        serializer = ProductsSerializer(
            new_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductsSerializer(
                product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a product

        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)
        product.name = request.data["name"]
        product.price = request.data["price"]
        product.description = request.data["description"]
        product.quantity = request.data["quantity"]
        product.location = request.data["location"]
        product.image_path = request.data["image_path"]
        product.customer_id = request.data["customer_id"]
        product.product_type_id = request.data["product_type_id"]
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to products resource

        Returns:
            Response -- JSON serialized list of products
        """
        customer_id = request.auth.user.customer.id
        products = Product.objects.all()

        product_name = self.request.query_params.get('name', None)
        product_location = self.request.query_params.get('location', None)
        is_one_customer = self.request.query_params.get('customer', False)
        if is_one_customer == 'true':
            products = products.filter(customer__id=customer_id)

        if product_name is not None:
            products = products.filter(name=product_name)

        if product_location is not None:
            products = products.filter(location=product_location)
        serializer = ProductsSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)
