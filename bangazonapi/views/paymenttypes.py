from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import PaymentType


class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    '''
    JSON serializer for payment types

    Arguments: serializers.HyperlinkedModelSerializer

    Author: Lauren Riddle

    '''

    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'merchant_name', 'account_number',  'expiration_date', 'customer')

class PaymentTypes(ViewSet):
    '''
    Payment Types for Bangazon 

    This class houses functions for List, Retrieve, Destroy, and Create

    Author: Lauren Riddle
    '''

    def retrieve(self, request):
        '''
        Handles GET requests for a single payment type

        Returns:
            Response --- JSON serialized PaymentTypes instance

        '''
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        '''
        Handles POST operations

        Returns: 
            Response --- JSON serialized PaymentTypes instance
        '''
        newpaymenttype = PaymentType()
        newpaymenttype.merchant_name = request.data['merchant_name']
        newpaymenttype.account_number = request.data['account_number']
        newpaymenttype.expiration_date = request.data['expiration_date']
        newpaymenttype.customer_id = request.auth.user.id

        newpaymenttype.save()

        serializer = PaymentTypeSerializer(newpaymenttype, context ={'request': request})

        return Response(serializer.data)
    

    def list(self, request):
        '''
        Handles the GET all requstes to the payment types resource

        Returns: 
        Response -- JSON serialized list of Payment Types

        Author: Lauren Riddle
        '''
        # list payment types
        types = PaymentType.objects.all()

        # take repsonse and covert to JSON
        serializer = PaymentTypeSerializer(types, many=True, context={'request': request})

        # return repsonse as JSON
        return Response(serializer.data)

    def destroy(self, request):
        '''
        Handles DELETE request for a single payment type

        Returns:
            Response -- 200, 404, or 500 status code

        Author: Lauren Riddle

        '''

        try: 
            type = PaymentType.objects.get(pk=pk)
            type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

