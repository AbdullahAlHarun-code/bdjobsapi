from rest_framework import serializers

class JobSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    company_logo_url = serializers.URLField(required=False)
    position = serializers.CharField(max_length=255)
    job_url = serializers.URLField()
    scraped_date = serializers.DateTimeField()