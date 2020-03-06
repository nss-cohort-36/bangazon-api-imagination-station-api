from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonapi.models.orderproducts import OrderProduct
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from bangazonapi.models import Product, Customer, ProductType, Order, PaymentType, Product



print("test file loaded------------------------")


class TestOrderProducts(TestCase):
    # used to get user auth to work
    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)

        self.customer = Customer.objects.create(user_id=1)
        self.product_type = ProductType.objects.create(name="type for testing")
        self.payment_type = PaymentType.objects.create(merchant_name="Visa", account_number="1234567", created_at="2020-03-04 20:41:57.004509", customer_id=self.customer.id, expiration_date="3020-12-31")

        self.order = Order.objects.create(
            created_at="2020-02-24 15:32:15.551752", 
            customer_id=self.customer.id, 
            payment_type_id=self.payment_type.id
        )

        self.product = Product.objects.create(
            name = "Hot Dog",
            price = 3.00,
            description = "Real good, fresh and not expired.",
            quantity = 11,
            location = "Franklin",
            image_path = "./none_pic.jpg",
            customer_id = self.customer.id,
            product_type_id = self.product_type.id
        )

    def test_post_order_product(self):
        # define a order product to be sent to the API
        new_order_product = {
              "order_id": self.order.id,
              "product_id": self.product.id
            }
        
        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('orderproduct-list'), new_order_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one order product instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(OrderProduct.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, order.
        self.assertEqual(OrderProduct.objects.get().product.id, 1)

    def test_get_order_product(self):
        new_order_product = OrderProduct.objects.create(
            order_id = self.order.id,
            product_id = self.product.id
        )

        # Now we can grab all the order product (meaning the one we just created) from the db
        response = self.client.get(reverse('orderproduct-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one product type in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["order"]["id"], 1)

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_order_product.product.name.encode(), response.content)

        print("HELP", )


if __name__ == '__main__':
    unittest.main()