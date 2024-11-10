"""
Test Factory to make fake objects for testing
"""

from datetime import date
from factory import Factory, Sequence, Faker
from service.models import Product
from factory.fuzzy import FuzzyInteger, FuzzyFloat, FuzzyChoice


class ProductFactory(Factory):
    """Creates fake products that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = Sequence(lambda n: n)
    name = Faker("name")
    # price = FuzzyInteger(10, 50)
    price = FuzzyFloat(10.0, 50.0)
    description = Faker("text")
    imageUrl = Faker("image_url")
    available = FuzzyChoice([True, False])
    # Todo: Add your other attributes here...
