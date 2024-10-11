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
#  R E S T   A P I   E N D P O I N T S
######################################################################


@app.route("/products", methods=["GET"])
def list_products():
    """Returns all of the Products"""
    app.logger.info("Request for product list")

    products = []

    # parse the query request
    name = request.args.get("name")

    # TODO: support more query methods and test them

    # price = request.args.get("price")
    # img_url = request.args.get("imageUrl")

    print(request.args)

    if name:
        app.logger.info(f"Finding by name: {name}")
        products = Product.find_by_name(name)

    results = [product.serialize() for product in products]
    app.logger.info(f"Find {len(results)} products")
    return jsonify(results), status.HTTP_200_OK


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

    # TODO: uncomment this when read API is implemented!
    # location_url = url_for("get_products", product_id=product.id, _external=True)

    location_url = "JUST A TEST FOR CREATE!"

    return (
        jsonify(product.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a product

    This endpoint will delete a product based on the ID specified in the path.
    """
    app.logger.info("Request to delete a product with ID [%s]", product_id)

    # Find the product by ID
    product = Product.find(product_id)
    if product:
        app.logger.info("Product with ID: %d found.", product.id)
        product.delete()

    app.logger.info("Product with ID: %d deletion complete.", product_id)
    return {}, status.HTTP_204_NO_CONTENT


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
