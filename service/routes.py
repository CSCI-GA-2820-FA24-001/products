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
Product Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Product

Product Store Service with Swagger

Paths:
------
GET / - Displays a UI for Selenium testing
GET /products - Returns a list all of the Products
GET /products/{id} - Returns the Product with a given id number
POST /products - creates a new Product record in the database
PUT /products/{id} - updates a Product record in the database
DELETE /products/{id} - deletes a Product record in the database
"""

from decimal import Decimal
from flask import current_app as app  # Import Flask application
from flask import jsonify
from flask_restx import Resource, fields, reqparse, inputs
from service.models import Product
from service.common import status  # HTTP Status Codes
from . import api


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return app.send_static_file("index.html")


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health", methods=["GET"])
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


create_model = api.model(
    "Product",
    {
        "id": fields.Integer(required=True, description="ID of the product"),
        "name": fields.String(required=True, description="The name of the Product"),
        "description": fields.String(
            required=True,
            description="The category of Product (e.g., dog, cat, fish, etc.)",
        ),
        "available": fields.Boolean(
            required=True, description="Is the Product available for purchase?"
        ),
        "price": fields.Float(required=True, description="The price of the Product"),
        "image_url": fields.String(
            required=False, description="The URL of the product image"
        ),
    },
)

product_model = api.inherit(
    "ProductModel",
    create_model,
    {
        "_id": fields.String(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument(
    "name", type=str, location="args", required=False, help="List Products by name"
)
product_args.add_argument(
    "description",
    type=str,
    location="args",
    required=False,
    help="List Products by category",
)
product_args.add_argument(
    "available",
    type=inputs.boolean,
    location="args",
    required=False,
    help="List Products by availability",
)
product_args.add_argument(
    "price",
    type=Decimal,
    location="args",
    required=False,
    help="List Products by price",
)


######################################################################
#  PATH: /products/{id}
######################################################################
@api.route("/products/<product_id>")
@api.param("product_id", "The Product identifier")
class ProductResource(Resource):
    """
    ProductResource class

    Allows the manipulation of a single Product
    GET /product{id} - Returns a Product with the id
    PUT /product{id} - Update a Product with the id
    DELETE /product{id} -  Deletes a Product with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A PRODUCT
    # ------------------------------------------------------------------
    @api.doc("get_products")
    @api.response(404, "Product not found")
    @api.marshal_with(product_model)
    def get(self, product_id):
        """
        Retrieve a single Product

        This endpoint will return a Product based on its id
        """
        app.logger.info("Request to Retrieve a product with id [%s]", product_id)

        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found.",
            )

        app.logger.info("Returning product: %s", product.name)
        return product.serialize(), status.HTTP_200_OK

    ######################################################################
    # UPDATE AN EXISTING PRODUCT
    ######################################################################
    @api.doc("update_products")
    @api.response(404, "Product not found")
    @api.response(400, "The posted Product data was not valid")
    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, product_id):
        """
        Update a Product

        This endpoint will update a Product based the body that is posted
        """
        app.logger.info("Request to Update a product with id [%s]", product_id)
        # check_content_type("application/json")

        # Attempt to find the Product and abort if not found
        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found.",
            )

        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        product.deserialize(data)
        product.id = product_id
        product.update()
        app.logger.info("Product with ID: %d updated.", product.id)
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A PRODUCT
    # ------------------------------------------------------------------
    @api.doc("delete_products")
    @api.response(204, "Product deleted")
    def delete(self, product_id):
        """
        Delete a Product

        This endpoint will delete a Product based the id specified in the path
        """
        app.logger.info("Request to Delete a product with id [%s]", product_id)
        product = Product.find(product_id)
        if product:
            app.logger.info("Product with ID: %d found.", product.id)
            product.delete()
        app.logger.info("Product with ID: %d delete complete.", product_id)
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /products
######################################################################
@api.route("/products", strict_slashes=False)
class ProductCollection(Resource):
    """Handles all interactions with collections of Products"""

    # ------------------------------------------------------------------
    # LIST ALL PRODUCTS
    # ------------------------------------------------------------------
    @api.doc("list_products")
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """Returns all of the Products"""
        app.logger.info("Request to list Products...")
        products = []
        args = product_args.parse_args()
        if args["description"]:
            app.logger.info("Filtering by description: %s", args["description"])
            products = Product.find_by_description(args["description"])
        elif args["name"]:
            app.logger.info("Filtering by name: %s", args["name"])
            products = Product.find_by_name(args["name"])
        elif args["available"]:
            app.logger.info("Filtering by availability: %s", args["available"])
            products = Product.find_by_availability(args["available"])
        elif args["price"]:
            app.logger.info("Filtering by price: %s", args["price"])
            products = Product.find_by_price(Decimal(args["price"]))
        else:
            app.logger.info("Returning unfiltered list.")
            products = Product.all()

        # app.logger.info("[%s] Products returned", len(products))
        results = [product.serialize() for product in products]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW PRODUCT
    # ------------------------------------------------------------------
    @api.doc("create_products")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Creates a Product
        This endpoint will create a Product based the data in the body that is posted
        """
        app.logger.info("Request to Create a Product")
        product = Product()
        app.logger.debug("Payload = %s", api.payload)
        product.deserialize(api.payload)
        product.create()
        app.logger.info("Product with new id [%s] created!", product.id)
        location_url = api.url_for(
            ProductResource, product_id=product.id, _external=True
        )
        return product.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /products/{id}/purchase
######################################################################
@api.route("/products/<product_id>/purchase")
@api.param("product_id", "The Product identifier")
class PurchaseResource(Resource):
    """Purchase actions on a Product"""

    @api.doc("purchase_products")
    @api.response(404, "Product not found")
    @api.response(409, "The Product is not available for purchase")
    def put(self, product_id):
        """
        Purchase a Product

        This endpoint will purchase a Product and make it unavailable
        """
        app.logger.info("Request to Purchase a Product")
        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id [{product_id}] was not found.",
            )
        if not product.available:
            abort(
                status.HTTP_409_CONFLICT,
                f"Product with id [{product_id}] is not available.",
            )
        product.available = False
        product.update()
        app.logger.info("Product with id [%s] has been purchased!", product.id)
        return product.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)


def data_reset():
    """Removes all Products from the database"""
    Product.remove_all()
