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
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Product
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Product REST API Service",
            version="1.0",
            path=url_for("list_products", _external=True),
        ),
        status.HTTP_200_OK,
    )


@app.route("/health", methods=["GET"])
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING PET
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product

    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to Update a product with id [%s]", product_id)
    check_content_type("application/json")

    # Attempt to find the Product and abort if not found
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    # Update the Product with the new data
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    product.deserialize(data)

    # Save the updates to the database
    product.update()

    app.logger.info("Product with ID: %d updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# CREATE A NEW PRODUCT
######################################################################


@app.route("/products", methods=["POST"])
def create_products():
    """
    Create a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")

    product = Product()

    data = request.get_json()
    app.logger.info(f"Deserializing data {data}")
    product.deserialize(data)
    product.create()
    app.logger.info(f"Product {product.id}: {product.name} is saved!")

    location_url = url_for("get_products", product_id=product.id, _external=True)

    return (
        jsonify(product.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# LIST ALL PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns Products based on name and price"""
    app.logger.info("Request for product list")

    name = request.args.get("name")
    price = request.args.get("price")

    query = Product.query

    if name:
        app.logger.info("Find by name (fuzzy match): %s", name)
        query = query.filter(Product.name.like(f"%{name}%"))

    if price:
        try:
            app.logger.info("Find by price range: %s", price)
            price_value = float(price)
            query = query.filter(
                Product.price.between(price_value - 5, price_value + 5)
            )
        except ValueError:
            app.logger.error("Invalid price format: %s", price)
            return (
                jsonify({"error": "Invalid price format"}),
                status.HTTP_400_BAD_REQUEST,
            )

    products = query.all()

    if not products:
        return jsonify({"message": "No products found"}), status.HTTP_404_NOT_FOUND

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product

    This endpoint will return a Product based on its id
    """
    app.logger.info("Request to Retrieve a product with id [%s]", product_id)

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
