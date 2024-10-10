######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Test cases for Product Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import Product, DataValidationError, db
from .factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  PRODUCT   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCaseBase(TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S   FOR   CRUD
    ######################################################################

    def test_create_a_product(self):
        """It should create a new product"""
        product = Product(
            name="book", description="It's a book", price=15.2, imageUrl="www.test.com"
        )
        self.assertEqual(str(product), "<Product book id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "book")
        self.assertEqual(product.description, "It's a book")
        self.assertTrue(isinstance(product.price, float), True)
        self.assertEqual(str(product.price), "15.2")
        self.assertEqual(product.imageUrl, "www.test.com")

    def test_create_and_add_a_product(self):
        """It should create a product and add it into db"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)
        found = Product.all()
        self.assertEqual(len(found), 1)
        data = Product.find(product.id)
        self.assertEqual(data.name, product.name)
        self.assertEqual(data.description, product.description)
        self.assertEqual(data.price, product.price)
        self.assertEqual(data.imageUrl, product.imageUrl)

    def test_update_a_pet(self):
        """It should Update a Product"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        logging.debug(product)
        self.assertIsNotNone(product.id)
        # Change it and save it
        product.name = "new_name"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.name, "new_name")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].name, "new_name")

    def test_update_no_id(self):
        """It should not Update a Product with no id"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        self.assertRaises(DataValidationError, product.update)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCase):
    """Product Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        product = ProductFactory()
        self.assertRaises(DataValidationError, product.update)

    # TODO

    ######################################################################
    #  T E S T   C A S E S   FOR   SERIALIZE/DESERIALIZE
    ######################################################################
    def test_serialize_a_product(self):
        """It should serialize a product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("description", data)
        self.assertEqual(data["description"], product.description)
        self.assertIn("price", data)
        self.assertEqual(data["price"], product.price)
        self.assertIn("imageUrl", data)
        self.assertEqual(data["imageUrl"], product.imageUrl)

    def test_deserialize_a_product(self):
        """It should de-serialize a Product"""
        data = {
            "name": "Sample Product",
            "description": "A sample description",
            "price": 19.99,
            "imageUrl": "http://example.com/image.png",
        }
        product = Product()  # Assuming 'Product' is the new class name instead of 'Pet'
        product.deserialize(data)
        self.assertIsNotNone(product)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.description, data["description"])
        self.assertEqual(product.price, data["price"])
        self.assertEqual(product.imageUrl, data["imageUrl"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Product with missing data"""
        data = {
            "name": "Sample Product",
            "price": 19.99,
        }  # Missing description and imageUrl
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"  # Invalid data type
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_price(self):
        """It should not deserialize a bad price attribute"""
        test_product = ProductFactory()
        data = test_product.serialize()
        data["price"] = "19.99"  # Invalid price, should be a float
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCaseBase):
    """Product Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        product = ProductFactory()
        self.assertRaises(DataValidationError, product.create)
