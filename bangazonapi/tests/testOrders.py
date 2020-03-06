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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().customer.id, 1)

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

    def test_delete_order(self):
        """TEST for destroy method on order view"""
        new_order = Order.objects.create(
            customer_id=self.customer.id,
            payment_type_id=self.payment_type.id
        )

        # Delete a product. As shown in our post and get tests above, new_product
        # will be the only product in the database, and will have an id of 1
        response = self.client.delete(
            reverse('order-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 204)

        # Confirm that the product is NOT in the database, which means no products will be
        response = self.client.get(reverse('order-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        self.assertEqual(len(response.data), 0)

if __name__ == '__main__':
    unittest.main()
