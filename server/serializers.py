from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    sales_data = serializers.FileField()
