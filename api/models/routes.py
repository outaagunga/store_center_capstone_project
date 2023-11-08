# app.py

from flask import request, jsonify, make_response, session, redirect
from flask_migrate import Migrate
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from collections import OrderedDict
from models.user import User
from models.order import Order
from models.database import db, app
from models.storagespace import StorageSpace
from models.review import Review


# Home Page
@app.route('/')
def home():
    Welcome_to_Jeco_API_Endpoints = {
        "User Endpoints": {
            "GET /users": "Retrieve a list of users.",
            "GET /user/{user_id}": "Retrieve a specific user by user_id.",
            "POST /user": "Create a new user.",
            "PUT /user/{user_id}": "Update a specific user by user_id.",
            "DELETE /user/{user_id}": "Delete a specific user by user_id.",
        },
        "Orders Endpoints": {
            "GET /orders": "Retrieve a list of orders.",
            "GET /order/{order_id}": "Retrieve a specific order by order_id.",
            "POST /order": "Create a new order.",
            "PUT /order/{order_id}": "Update a specific order by order_id.",
            "DELETE /order/{order_id}": "Delete a specific order by order_id.",
        },
        # "Customers Endpoints": {
        #     "GET /customers": "Retrieve a list of customers.",
        #     "GET /customers/{customer_id}": "Retrieve a specific customer by customer_id.",
        #     "POST /customers": "Create a new customer.",
        #     "PUT /customers/{customer_id}": "Update a specific customer by customer_id.",
        #     "DELETE /customers/{customer_id}": "Delete a specific customer by customer_id.",
        # },
        "Storage Space Endpoints": {
            "GET /space": "Retrieve a list of storage spaces.",
            "GET /space/{storage_space_id}": "Retrieve a specific storage space by storage_space_id.",
            "POST /space": "Create a new storage space.",
            "PUT /space/{storage_space_id}": "Update a specific storage space by storage_space_id.",
            "DELETE /space/{storage_space_id}": "Delete a specific storage space by storage_space_id.",
        },
        # "Order Status Endpoints": {
        #     "GET /order_statuses": "Retrieve a list of order statuses.",
        #     "GET /order_statuses/{status_id}": "Retrieve a specific order status by status_id.",
        #     "POST /order_statuses": "Create a new order status.",
        #     "PUT /order_statuses/{status_id}": "Update a specific order status by status_id.",
        #     "DELETE /order_statuses/{status_id}": "Delete a specific order status by status_id.",
        # },
        "Transactions Endpoints": {
            "GET /transactions": "Retrieve a list of transactions.",
            "GET /transaction/{transaction_id}": "Retrieve a specific transaction by transaction_id.",
            "POST /transaction/{transaction_id}": "Create a new transaction.",
            "PUT /transaction/{transaction_id}": "Update a specific transaction by transaction_id.",
            "DELETE /transaction/{transaction_id}": "Delete a specific transaction by transaction_id.",
        },
        "Files Endpoints": {
            "GET /files": "Retrieve a list of files.",
            "GET /files/{file_id}": "Retrieve a specific file by file_id.",
            "POST /files": "Upload a new file.",
            "PUT /files/{file_id}": "Update a specific file by file_id.",
            "DELETE /files/{file_id}": "Delete a specific file by file_id.",
        },
        "Receipts Endpoints": {
            "GET /receipts": "Retrieve a list of receipts.",
            "GET /receipts/{receipt_id}": "Retrieve a specific receipt by receipt_id.",
            "POST /receipts": "Create a new receipt.",
            "PUT /receipts/{receipt_id}": "Update a specific receipt by receipt_id.",
            "DELETE /receipts/{receipt_id}": "Delete a specific receipt by receipt_id.",
        },
        # "To Be Received Items Endpoints": {
        #     "GET /to_be_received_items": "Retrieve a list of items to be received.",
        #     "GET /to_be_received_items/{to_be_received_id}": "Retrieve a specific item to be received by to_be_received_id.",
        #     "POST /to_be_received_items": "Create a new item to be received.",
        #     "PUT /to_be_received_items/{to_be_received_id}": "Update a specific item to be received by to_be_received_id.",
        #     "DELETE /to_be_received_items/{to_be_received_id}": "Delete a specific item to be received by to_be_received_id.",
        # # },
        # "To Be Picked Items Endpoints": {
        #     "GET /to_be_picked_items": "Retrieve a list of items to be picked.",
        #     "GET /to_be_picked_items/{to_be_picked_id}": "Retrieve a specific item to be picked by to_be_picked_id.",
        #     "POST /to_be_picked_items": "Create a new item to be picked.",
        #     "PUT /to_be_picked_items/{to_be_picked_id}": "Update a specific item to be picked by to_be_picked_id.",
        #     "DELETE /to_be_picked_items/{to_be_picked_id}": "Delete a specific item to be picked by to_be_picked_id.",
        # },
        "Reviews Endpoints": {
            "GET /reviews": "Retrieve a list of reviews.",
            "GET /reviews/{review_id}": "Retrieve a specific review by review_id.",
            "POST /reviews": "Create a new review.",
            "PUT /reviews/{review_id}": "Update a specific review by review_id.",
            "DELETE /reviews/{review_id}": "Delete a specific review by review_id.",
        },
        "Discounts Endpoints": {
            "GET /discounts": "Retrieve a list of discounts.",
            "GET /discounts/{discount_id}": "Retrieve a specific discount by discount_id.",
            "POST /discounts": "Create a new discount.",
            "PUT /discounts/{discount_id}": "Update a specific discount by discount_id.",
            "DELETE /discounts/{discount_id}": "Delete a specific discount by discount_id.",
        },
        "Pickup Service Endpoints": {
            "GET /pickup_services": "Retrieve a list of pickup services.",
            "GET /pickup_services/{pickup_service_id}": "Retrieve a specific pickup service by pickup_service_id.",
            "POST /pickup_services": "Create a new pickup service.",
            "PUT /pickup_services/{pickup_service_id}": "Update a specific pickup service by pickup_service_id.",
            "DELETE /pickup_services/{pickup_service_id}": "Delete a specific pickup service by pickup_service_id.",
        },
        "Notifications Endpoints": {
            "GET /notifications": "Retrieve a list of notifications.",
            "GET /notifications/{notification_id}": "Retrieve a specific notification by notification_id.",
            "POST /notifications": "Create a new notification.",
            "PUT /notifications/{notification_id}": "Update a specific notification by notification_id.",
            "DELETE /notifications/{notification_id}": "Delete a specific notification by notification_id.",
        },
        "Logs Endpoints": {
            "GET /logs": "Retrieve a list of logs.",
            "GET /logs/{log_id}": "Retrieve a specific log by log_id.",
            "POST /logs": "Create a new log entry.",
            "PUT /logs/{log_id}": "Update a specific log entry by log_id.",
            "DELETE /logs/{log_id}": "Delete a specific log entry by log_id.",
        },
        "Closed Orders Endpoints": {
            "GET /closed_orders": "Retrieve a list of closed orders.",
            "GET /closed_orders/{closed_order_id}": "Retrieve a specific closed order by closed_order_id.",
            "POST /closed_orders": "Create a new closed order entry.",
            "PUT /closed_orders/{closed_order_id}": "Update a specific closed order entry by closed_order_id.",
            "DELETE /closed_orders/{closed_order_id}": "Delete a specific closed order entry by closed_order_id.",
        }},

    return jsonify(Welcome_to_Jeco_API_Endpoints)
