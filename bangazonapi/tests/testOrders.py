from django.test import TestCase
from django.urls import reverse
from bangazonapi.models import Customer, PaymentType, Order
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip

print("test orders file loaded-----------------")


class TestOrders(TestCase):
    # used to get user auth to work
    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1)
        self.payment_type = PaymentType.objects.create(
            merchant_name='Visa',
            account_number='1111 1111 1111 1111',
            expiration_date='2020-09-30',
            customer_id=self.customer.id)

    @skip
    def test_post_order(self):
        # define an order to be sent to the API
        new_order = {
            "customer": self.customer.id,
            "payment_type": self.payment_type.id
        }
        
        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('order-list'), new_order, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one Product Type instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(Order.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(Order.objects.get().customer.id, 1)

    @skip
    def test_get_order(self):
        new_order = Order.objects.create(
            customer_id=self.customer.id,
            payment_type_id=self.payment_type.id
        )

        # Now we can grab all the product types (meaning the one we just created) from the db
        response = self.client.get(reverse('order-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["customer"]["id"], 1)
        self.assertIn(new_order.customer.encode(), response.content)


if __name__ == '__main__':
    unittest.main()