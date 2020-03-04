"""Customers view """
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from bangazonapi.models import Customer

#! This is a nested serialzer; PAY ATTENTION

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for users

    Arguments:
        serializers
    """
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        fields = ('id', 'url', 'username', 'last_name', 'first_name', 'email')
       
class CustomersSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers

    Arguments:
        serializers
    """

    user = UsersSerializer()

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        depth = 2
        fields = ('id', 'user', 'address', 'city', 'phone', 'zipcode')

class Users(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user instance
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UsersSerializer(
                user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class Customers(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomersSerializer(
                customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to customers resource
        Returns:
            Response -- JSON serialized list of customers
        """      
        customers = Customer.objects.filter(id = request.auth.user.customer.id)

        customer = self.request.query_params.get('customer', None)

        if customer is not None:
            customers = customers.filter(id=customer)

        serializer = CustomersSerializer(customers, many = True, context={'request': request})

        return Response(serializer.data)