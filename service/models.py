"""
Models for Product

All of the models are stored in this module
"""

import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Product(db.Model):
    """
    Class that represents a Product
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    imageUrl = db.Column(db.String(255), nullable=False)

    # #maybe we need this attribute?
    # in_stock = db.Column(
    #     db.Boolean(), nullable=False, default=False
    # )

    # Todo: Place the rest of your schema here...

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a ProductModel to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a ProductModel to the database
        """
        logger.info("Saving %s", self.name)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a ProductModel from the data store"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "imageUrl": self.imageUrl,
        }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.description = data["description"]
            price = data["price"]
            if not isinstance(price, float):
                raise DataValidationError("Invalid type for price: must be a float")
            self.price = price
            self.imageUrl = data["imageUrl"]
        # except AttributeError as error:
        #     raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Product: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Products in the database"""
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find_by_id(cls, product_id):
        """Returns the Product with the given id

        Args:
            product_id (int): the id of the Product you want to retrieve
        """
        logger.info("Processing ID look up for id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name

        Args:
            name (string): the name of the Products you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_description(cls, description):
        """Returns all Products with the given description

        Args:
            description (string): the description of the Products you want to match
        """
        logger.info("Processing description query for %s ...", description)
        return cls.query.filter(cls.description == description).all()

    @classmethod
    def find_by_price(cls, price):
        """Returns all Products with the given price

        Args:
            price (float): the price of the Products you want to match
        """
        logger.info("Processing price query for %s ...", price)
        return cls.query.filter(cls.price == price).all()

    @classmethod
    def find_by_imageUrl(cls, imageUrl):
        """Returns all Products with the given imageUrl

        Args:
            imageUrl (string): the image URL of the Products you want to match
        """
        logger.info("Processing imageUrl query for %s ...", imageUrl)
        return cls.query.filter(cls.imageUrl == imageUrl).all()

    # @classmethod
    # def find_by_in_stock(cls, in_stock: bool = True) -> list:
    #     """Returns all Products by their stock status

    #     :param in_stock: True for products that are in stock
    #     :type in_stock: bool

    #     :return: a collection of Products that are in stock
    #     :rtype: list

    #     """
    #     if not isinstance(in_stock, bool):
    #         raise TypeError("Invalid stock status, must be of type boolean")
    #     logger.info("Processing stock query for %s ...", in_stock)
    #     return cls.query.filter(cls.in_stock == in_stock)
