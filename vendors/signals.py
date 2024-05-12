import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from vendors.models import PurchaseOrder, Vendor, HistoricalPerformance
from django.db.models import Avg, Count
from django.utils import timezone

logger = logging.getLogger(__name__)


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    try:
        vendor = instance.vendor
        if instance.status == 'completed':
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
            total_orders_count = purchase_orders.count()
            completed_orders = purchase_orders.filter(status='completed')
            completed_orders_count = completed_orders.count()
            fulfilment_rate = completed_orders_count / total_orders_count if total_orders_count != 0 else 0
            on_time_orders = 0
            rating_sum = 0
            for order in completed_orders:
                if order.delivery_date == order.expected_delivery_date:
                    on_time_orders += 1
                rating_sum += order.quality_rating
            if completed_orders_count > 0:
                on_time_delivery_rate = on_time_orders / completed_orders_count
                quality_rating_avg = rating_sum / completed_orders_count
            else:
                on_time_delivery_rate = 0.0
                quality_rating_avg = 0.0

            vendor.quality_rating_avg = quality_rating_avg
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.fulfilment_rate = fulfilment_rate
            vendor.save()

            logger.info(f"creating history of performance of vendor {vendor}")
            HistoricalPerformance.objects.create(
                vendor=vendor,
                date=timezone.now().date(),
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_avg,
                average_response_time=vendor.average_response_time,
                fulfilment_rate=vendor.fulfilment_rate
            )
    except Exception as e:
        logger.error(f"An error occurred while updating vendor performance: {e}")