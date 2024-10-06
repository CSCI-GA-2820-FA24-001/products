"""
Test Factory to make fake objects for testing
"""
from datetime import date
from factory import Factory, Sequence, Faker
from service.models import Product
from factory.fuzzy import FuzzyInteger

class ProductFactory(Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = Sequence(lambda n: n)
    name = Faker("name")
    price = FuzzyInteger(10, 50)
    description = Faker("text")
    imageUrl = Faker("image_url") 



    # Todo: Add your other attributes here...