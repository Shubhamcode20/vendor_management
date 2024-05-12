from django.shortcuts import render, get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor, PurchaseOrder
from .services.commands import create_vendor, update_vendor, delete_vendor, create_purchase_order, \
    update_purchase_order, delete_purchase_order, get_vendor_performance, update_acknowledgement_date
from .services.queries import get_vendors, get_purchase_orders


class VendorApi(APIView):

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        contact_details = serializers.CharField()
        address = serializers.CharField()
        vendor_code = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        contact_details = serializers.CharField()
        address = serializers.CharField()
        vendor_code = serializers.CharField()
        on_time_delivery_rate = serializers.FloatField()
        quality_rating_avg = serializers.FloatField()
        average_response_time = serializers.FloatField()
        fulfillment_rate = serializers.FloatField()

    def get(self, request, *args, **kwargs):
        if 'vendor_id' in kwargs:
            vendor = get_object_or_404(Vendor, id=kwargs['vendor_id'])
            return Response(self.OutputSerializer(vendor).data, status=status.HTTP_200_OK)
        vendors = get_vendors()
        return Response(self.OutputSerializer(vendors, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        vendor = create_vendor(**serializer.validated_data)
        return Response(self.OutputSerializer(vendor).data, status=status.HTTP_201_CREATED)

    def put(self, request, vendor_id,  *args, **kwargs):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        serializer = self.InputSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        vendor = update_vendor(vendor=vendor, **serializer.validated_data)
        return Response(self.OutputSerializer(vendor).data, status=status.HTTP_200_OK)

    def delete(self, request, vendor_id, *args, **kwargs):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        delete_vendor(vendor=vendor)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderApi(APIView):

    class InputSerializer(serializers.Serializer):
        po_number = serializers.CharField()
        vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())
        order_date = serializers.DateTimeField()
        delivery_date = serializers.DateTimeField()
        items = serializers.JSONField()
        quantity = serializers.IntegerField()
        status = serializers.CharField()
        quality_rating = serializers.FloatField(allow_null=True, required=False)
        issue_date = serializers.DateTimeField()
        expected_delivery_date = serializers.DateTimeField(required=True)
        acknowledgment_date = serializers.DateTimeField(allow_null=True, required=False)

    class OutputSerializer(serializers.Serializer):
        po_number = serializers.CharField()
        vendor = serializers.IntegerField(source='vendor.id')
        order_date = serializers.DateTimeField()
        delivery_date = serializers.DateTimeField()
        items = serializers.JSONField()
        quantity = serializers.IntegerField()
        status = serializers.CharField()
        quality_rating = serializers.FloatField()
        issue_date = serializers.DateTimeField()
        expected_delivery_date = serializers.DateTimeField()
        acknowledgment_date = serializers.DateTimeField()

    def get(self, request, *args, **kwargs):
        if 'purchase_order_id' in kwargs:
            purchase_order = get_object_or_404(PurchaseOrder, id=kwargs['purchase_order_id'])
            return Response(self.OutputSerializer(purchase_order).data, status=status.HTTP_200_OK)
        purchase_orders = get_purchase_orders()
        return Response(self.OutputSerializer(purchase_orders, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        purchase_order = create_purchase_order(**serializer.validated_data)
        return Response(self.OutputSerializer(purchase_order).data, status=status.HTTP_201_CREATED)

    def put(self, request, purchase_order_id, *args, **kwargs):
        purchase_order = get_object_or_404(PurchaseOrder, id=purchase_order_id)
        serializer = self.InputSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        purchase_order = update_purchase_order(purchase_order=purchase_order, **serializer.validated_data)
        return Response(self.OutputSerializer(purchase_order).data, status=status.HTTP_200_OK)

    def delete(self, request, purchase_order_id, *args, **kwargs):
        purchase_order = get_object_or_404(PurchaseOrder, id=purchase_order_id)
        delete_purchase_order(purchase_order=purchase_order)
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorPerformanceApi(APIView):
    class OutputSerializer(serializers.Serializer):

        class PerformaceSerializer(serializers.Serializer):
            on_time_delivery_rate = serializers.FloatField(source='vendor.on_time_delivery_rate')
            quality_rating_avg = serializers.FloatField(source='vendor.quality_rating_avg')
            average_response_time = serializers.FloatField(source='vendor.average_response_time')
            fulfilment_rate = serializers.FloatField(source='vendor.fulfilment_rate')
        vendor_id = serializers.IntegerField(source='vendor.id')
        vendor_name = serializers.CharField(source='vendor.name')


    def get(self, request, *args, **kwargs):
        vendor = get_object_or_404(Vendor, id=kwargs['vendor_id'])
        return Response(self.OutputSerializer(vendor).data, status=status.HTTP_200_OK)


class PurchaseOrderAcknowledgeApi(APIView):

    def post(self, request, purchase_order_id, *args, **kwargs):
        purchase_order = get_object_or_404(PurchaseOrder, id=purchase_order_id)
        update_acknowledgement_date(purchase_order=purchase_order)
