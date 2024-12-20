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
Module: error_handlers
"""
# from flask import jsonify
from flask import current_app as app  # Import Flask application
from service import api
from service.models import DataValidationError
from . import status


######################################################################
# Error Handlers
######################################################################


######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles Value Errors from bad data"""
    message = str(error)
    app.logger.error(message)
    return {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "error": "Bad Request",
        "message": message,
    }, status.HTTP_400_BAD_REQUEST


# @api.errorhandler(DataConnectionError)
# def database_connection_error(error):
#     """Handles Database Errors from connection attempts"""
#     message = str(error)
#     app.logger.critical(message)
#     return {
#         "status_code": status.HTTP_503_SERVICE_UNAVAILABLE,
#         "error": "Service Unavailable",
#         "message": message,
#     }, status.HTTP_503_SERVICE_UNAVAILABLE

# @api.errorhandler(DataValidationError)
# def request_validation_error(error):
#     """Handles Value Errors from bad data"""
#     return bad_request(error)


# @api.errorhandler(status.HTTP_400_BAD_REQUEST)
# def bad_request(error):
#     """Handles bad requests with 400_BAD_REQUEST"""
#     message = str(error)
#     app.logger.warning(message)
#     return (
#         jsonify(
#             status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message
#         ),
#         status.HTTP_400_BAD_REQUEST,
#     )

# @app.errorhandler(status.HTTP_404_NOT_FOUND)
# def not_found(error):
#     """Handles resources not found with 404_NOT_FOUND"""
#     message = str(error)
#     app.logger.warning(message)
#     return {
#         "status": status.HTTP_404_NOT_FOUND,
#         "error": "Not Found",
#         "message": message,
#     }, status.HTTP_404_NOT_FOUND


# @api.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
# def method_not_supported(error):
#     """Handles unsupported HTTP methods with 405_METHOD_NOT_SUPPORTED"""
#     message = str(error)
#     app.logger.warning(message)
#     return (
#         jsonify(
#             status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             error="Method not Allowed",
#             message=message,
#         ),
#         status.HTTP_405_METHOD_NOT_ALLOWED,
#     )


# @api.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
# def mediatype_not_supported(error):
#     """Handles unsupported media requests with 415_UNSUPPORTED_MEDIA_TYPE"""
#     message = str(error)
#     app.logger.warning(message)
#     return (
#         jsonify(
#             status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             error="Unsupported media type",
#             message=message,
#         ),
#         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#     )
