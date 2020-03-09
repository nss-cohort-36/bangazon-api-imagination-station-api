from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonapi.models.customers import Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip

print("test file loaded------------------------")


class TestCustomers(TestCase):
    # used to get user auth to work
    def setUp(self):

        self.username = 'testuser'
        self.password = 'foobar'
       
        self.user = User.objects.create_user(
            username = self.username, 
            password = self.password
        )
        self.customer = Customer.objects.create(
            user_id=1
        )

        self.token = Token.objects.create(user=self.user)
    
    # @skip
    def test_put_customer_update(self):
        # define a customer to be sent to the API
        new_customer_info = {
            "first_name": "Update Jim",
            "last_name": "Flippy update",
            "address": "123 Updated St",
            "city": "update City",
            "zipcode": "12345",
            "phone": "123-456-7890",
            "customer": 1
        }
        
        
        #  Use the client to send the request and store the response
        response = self.client.put(
        '/customers/profile_update', new_customer_info, content_type='application/json', HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 204)

        # Query the table to see if there's one customer instance in there. Since we are testing a PUT request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(Customer.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(User.objects.get().first_name, 'Update Jim')
        self.assertEqual(Customer.objects.get().zipcode, '12345')
    # @skip
    def test_get_customer(self):
        # new_customer = Customer.objects.create(
         
        # )

        # Now we can grab all the customers (meaning the one we just created) from the db
        response = self.client.get(
            reverse('customer-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialized data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one product type in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]['user']["username"], "testuser")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples

        # self.assertIn(new_customer.username.encode(), response.content)


if __name__ == '__main__':
    unittest.main()
