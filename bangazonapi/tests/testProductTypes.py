import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonapi.models.producttypes import ProductType

print("test file loaded------------------------")


class TestProductTypes(TestCase):
    def test_post_product_type(self):
        # define a product type to be sent to the API
        new_product_type = {
              "name": "Sporting Goods"
            }
        
        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('producttype-list'), new_product_type
          )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one Product Type instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(ProductType.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(ProductType.objects.get().name, 'Sporting Goods')

    # def test_get_parkareas(self):
    #     new_area = ParkArea.objects.create(
    #       name="Coaster Land",
    #       theme="coasters, duh",
    #     )

    #     # Now we can grab all the area (meaning the one we just created) from the db
    #     response = self.client.get(reverse('parkarea-list'))

    #     # Check that the response is 200 OK.
    #     # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
    #     self.assertEqual(response.status_code, 200)

    #     # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
    #     # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
    #     self.assertEqual(len(response.data), 1)

    #     # test the contents of the data before it's serialized into JSON
    #     self.assertEqual(response.data[0]["name"], "Coaster Land")

    #     # Finally, test the actual rendered content as the client would receive it.
    #     # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
    #     self.assertIn(new_area.name.encode(), response.content)


if __name__ == '__main__':
    unittest.main()