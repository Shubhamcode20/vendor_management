import logging
from vendors.models import Vendor, PurchaseOrder

logger = logging.getLogger(__name__)


def get_vendors():
    logger.info("Successfully retrieved all vendors.")
    vendors = Vendor.objects.all()
    return vendors


def get_purchase_orders():
    logger.info("Successfully retrieved all purchase orders.")
    purchase_orders = PurchaseOrder.objects.all()
    return purchase_orders
