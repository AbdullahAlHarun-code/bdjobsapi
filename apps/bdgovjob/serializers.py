from rest_framework import serializers
from .models import GovtJob


class GovtJobSerializer(serializers.ModelSerializer):
    """Serializer for Government Job data"""
    
    class Meta:
        model = GovtJob
        fields = [
            'id',
            'job_title',
            'job_url',
            'vacancies',
            'deadline',
            'posted_date',
            'scraped_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

