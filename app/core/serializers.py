from rest_framework import serializers
from datetime import datetime

class GeneralResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.DictField(allow_null=True)
    error = serializers.DictField(allow_null=True)
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", required=False)