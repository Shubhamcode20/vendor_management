
# Vendor Management System

The Vendor Management System is a Django-based system for managing vendors, tracking purchase orders, 
and calculating vendor performance metrics.

Creation of directory where i will keep my repository.

Create Django Project:
Workspace: vendor_management_system
Project repository: vendor_management

```bash
##create virtual environment:
python -m venv venv

## Activate the virtual environment:
venv\Scripts\activate

## Create Django Project (vendor_management):
django-admin startproject vendor_management

## Navigate into your project directory (vendor_management) and run the following command:
cd vendor_management

## Create Django App (vendors):
python manage.py startapp vendors

## Implement Models:
Inside the vendors app, we have to create the models mentioned in assignment(Vendor, PurchaseOrder, HistoricalPerformance). 
Define these models in models.py file of the vendors app.

## Migrate Command after creation of all mentioned model:
python manage.py migrate

## Run Runserver command which gives logs:
python manage.py runserver

## create super user credentials and verify models by django admin-forms:
python manage.py createsuperuser

## Access the Django admin:
Visit http://localhost:8000/admin/ in your browser.
Log in with the superuser credentials created during installation.

##Implement Views:
Define APIViews for your API endpoints in views.py file within the vendors app. Each endpoint mentioned in the assignment 
(e.g., /api/vendors/, /api/purchase_orders/, /api/vendors/<int:vendor_id>/performance) have a corresponding view function.

## Implement Backend Logic:
Implement the backend logic for calculating performance metrics as described in the assignment.


 Visit http://localhost:8000/admin/ in your browser to access the Django admin and log in with the superuser credentials 
 created earlier.

## API Endpoints (Use the provided API endpoints to manage vendors, track purchase orders, and evaluate vendor performance.)

1. Vendor Profile Management:
   POST /api/vendors/: Create a new vendor.
   GET /api/vendors/: List all vendors.
   GET /api/vendors/<int:vendor_id>/: Retrieve details of a specific vendor.
   PUT /api/vendors/<int:vendor_id>/: Update details of a specific vendor.
   DELETE /api/vendors/<int:vendor_id>/: Delete a specific vendor.

2.Vendor Performance Evaluation:
   GET /api/vendors/<int:vendor_id>/performance/: Retrieve performance metrics for a specific vendor.

3. Purchase Order Tracking:
   POST /api/purchase_orders/: Create a new purchase order.
   GET /api/purchase_orders/: List all purchase orders.
   GET /api/purchase_orders/<int:purchase_order_id>/: Retrieve details of a specific purchase order.
   PUT /api/purchase_orders/<int:purchase_order_id>/: Update details of a specific purchase order.
   DELETE /api/purchase_orders/<int:purchase_order_id>/: Delete a specific purchase order.
   POST /api/purchase_orders/<int:purchase_order_id>/acknowledge/: Acknowledge a purchase order by a vendor.

These endpoints correspond to the provided views in your Django application and define the functionality for managing vendors, 
tracking purchase orders, and evaluating vendor performance.

## Authentication
Secure the API endpoints with token-based authentication as specified in the assignment. 
Use Django REST Framework's built-in authentication classes for this purpose.

## Error Handling and Validations
Implement error handling and validations to raise appropriate validation errors if inappropriate IDs or types are caught in the code.
Ensure to follow these setup instructions and API endpoint details to effectively use the Vendor Management System.


```
