import datetime
import logging
from datetime import timedelta
from django.utils import timezone
from vendors.models import Vendor, PurchaseOrder

logger = logging.getLogger(__name__)


def create_vendor(name: str, contact_details: str, address: str, vendor_code: str) -> Vendor:
    logger.info(f"creating vendor {name}")
    vendor = Vendor.objects.create(
        name=name, contact_details=contact_details,
        address=address, vendor_code=vendor_code
    )
    return vendor


def update_vendor(vendor: Vendor, name: str, contact_details: str, address: str, vendor_code: str) -> Vendor:
    logger.info(f"updating vendor {name}")
    vendor.name = name
    vendor.contact_details = contact_details
    vendor.address = address
    vendor.vendor_code = vendor_code
    vendor.save()
    return vendor


def delete_vendor(vendor: Vendor) -> None:
    logger.info(f"deleting vendor {vendor}")
    vendor.delete()
    return None


def create_purchase_order(po_number: str, vendor: Vendor, order_date: datetime,
                          delivery_date: datetime, items: dict, quantity: int,
                          status: str, quality_rating: float,  issue_date: datetime,
                          expected_delivery_date: datetime,
                          acknowledgment_date: datetime) -> PurchaseOrder:
    logger.info(f"creating purchase order {po_number}")
    purchase_order = PurchaseOrder.objects.crete(
        po_number=po_number,
        vendor=vendor,
        order_date=order_date,
        delivery_date=delivery_date,
        items=items,
        quantity=quantity,
        status=status,
        quality_rating=quality_rating,
        issue_date=issue_date,
        acknowledgment_date=acknowledgment_date
    )
    return purchase_order


def update_purchase_order(purchase_order: PurchaseOrder, po_number: str, vendor: Vendor,
                          order_date: datetime, delivery_date: datetime, items: dict,
                          quantity: int, status: str, quality_rating: float,
                          issue_date: datetime, acknowledgment_date: datetime):
    logger.info(f"updating purchase order {po_number}")
    purchase_order.po_number = po_number
    purchase_order.vendor = vendor
    purchase_order.order_date = order_date
    purchase_order.delivery_date = delivery_date
    purchase_order.items = items
    purchase_order.quantity = quantity
    purchase_order.status = status
    purchase_order.quality_rating = quality_rating
    purchase_order.issue_date = issue_date
    purchase_order.acknowledgment_date = acknowledgment_date
    purchase_order.save()
    return purchase_order


def delete_purchase_order(purchase_order: PurchaseOrder):
    logger.info(f"deleting purchase order {purchase_order}")
    purchase_order.delete()
    return


def get_vendor_performance(vendor: Vendor):
    return {
        "vendor_id": vendor.id,
        "vendor_name": vendor.name,
        "performance_metrics": {
            "on_time_delivery_rate": vendor.on_time_delivery_rate,
            "quality_rating_avg": vendor.quality_rating_avg,
            "average_response_time": vendor.average_response_time,
            "fulfilment_rate": vendor.fulfillment_rate
        }
    }


def calculate_average_response_time(vendor):
    logger.info(f"Calculation of average response time of vendor {vendor}")
    acknowledged_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    total_response_time = timedelta()

    for order in acknowledged_orders:
        response_time = order.acknowledgment_date - order.issue_date
        total_response_time += response_time

    average_response_time = total_response_time / acknowledged_orders.count() if acknowledged_orders.count() > 0 else timedelta(0)
    return average_response_time


def update_vendor_average_response_time(vendor):
    logger.info(f"Updating average response time of vendor {vendor}")
    average_response_time = calculate_average_response_time(vendor)
    vendor.average_response_time = average_response_time.total_seconds() / 3600
    vendor.save()


def update_acknowledgement_date(purchase_order: PurchaseOrder) -> PurchaseOrder:
    logger.info(f"Updating acknowledgement date of order {purchase_order}")
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()
    update_vendor_average_response_time(purchase_order.vendor)
    return purchase_order
