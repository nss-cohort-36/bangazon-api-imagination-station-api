from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonapi.models.paymenttypes import PaymentType
from bangazonapi.models.customers import Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



print("test file loaded------------------------")

class TestPaymentTypes(TestCase):
    # used for user auth
    def setUp(self):
        self.username = 'suiterNet'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1,
            address=23,
            city="Nashville",
            zipcode=1234214,
            phone=1234567890)

    def test_post_payment_type(self):
        # define a payment type to be POSTed to the DB
        new_payment_type = {
            "merchant_name": "Tacobell Discover Card",
            "account_number": "789",
            "expiration_date": "11/2020",
        }

        # use the client to send the request and store the response
        response = self.client.post(
            reverse('paymenttype-list'), new_payment_type, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

         # returns 200 back if we have a success with the test
        self.assertEqual(response.status_code, 200)

        # queries the table to see how many payment types are in it
        self.assertEqual(PaymentType.objects.count(), 1)

        # queries the table to make sure the object we just added is in there by checking one of the properties. In this case, merchant_name.
        self.assertEqual(PaymentType.objects.get().merchant_name, 'Tacobell Discover Card')

    def test_get_payment_type(self):
        # define a payment type to be POSTed to the DB
        new_payment_type = PaymentType.objects.create(
            merchant_name= "Tacobell Discover Card",
            account_number= "789",
            expiration_date= "11/2020",
            customer_id=1
        )
         

        # Now we can grab all the payment types (meaning the one we just created) from the db
        response = self.client.get(reverse('paymenttype-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one payment type in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["merchant_name"], "Tacobell Discover Card")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_payment_type.merchant_name.encode(), response.content)

    def test_delete_payment_type(self):
        # define a payment type to be POSTed to the DB
        new_payment_type = PaymentType.objects.create(
            merchant_name= "Tacobell Discover Card",
            account_number= "789",
            expiration_date= "11/2020",
            customer_id=1
        )
         
        # perform a delete on the object. Note: you have to reverse to paymenttype-detail sinces you are only targeting one object and not the whole list
        response = self.client.delete(reverse('paymenttype-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))
 
        # Check that the response is 204 OK.
        self.assertEqual(response.status_code, 204)

        # Now we can grab all the payment types from the db. In this case there should be 0
        response = self.client.get(reverse('paymenttype-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # test that the length of the response is 0, which means the delete was successful
        self.assertEqual(len(response.data), 0)

if __name__ == '__main__':
    unittest.main()

