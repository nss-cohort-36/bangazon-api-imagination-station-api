"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Order

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Order
        # creates a clickable url for the API
        url = serializers.HyperlinkedIdentityField(
            view_name="order",
            lookup_field='id'
        )
        fields = ('id', 'created_at', 'customer', 'payment_type')


class Orders(Viewset):
    """Orders for Bangazon API"""

    # Handles POST
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Order instance
        """
        new_order = Order()
        new_order.customer_id = request.auth.user.id
        new_order.save()

        serializer = OrderSerializer(
            new_order,
            context={'request': request}
            )

        return Response(serializer.data)

    
    # handles GET one ( the /<some_number in url tells it that)
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single order.

        Returns:
            Response -- JSON serialized Order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    # handles GET all
    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of orders
        """
        # list of order instances
        orders = Orders.objects.all()
        # takes orders and converts to JSON
        serializer = OrderSerializer(
            orders,
            many=True,
            context={'request': request}
        )
        # Return the JSON
        return Response(serializer.data)


    # handles PUT
    def update(self, request, pk=None):
        """Handle PUT requests for an order

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.payment_type_id = request.data["payment_type_id"]
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)