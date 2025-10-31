from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import HotJob


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotJob
        fields = ['id', 'company_name', 'company_logo_url', 'position', 'job_url', 'scraped_date', 'created_at']


class SendDataView(APIView):
    """POST: accept single or list of jobs and persist them."""

    def post(self, request):
        data = request.data
        payloads = data if isinstance(data, list) else [data]

        created = []
        errors = []
        skipped = []

        for item in payloads:
            serializer = JobSerializer(data=item)
            if not serializer.is_valid():
                errors.append(serializer.errors)
                continue

            vd = serializer.validated_data
            job_url = (vd.get('job_url') or '').strip()

            # Deduplication strategy:
            # 1) If job_url provided, consider it unique key.
            # 2) Otherwise, use company_name + position + scraped_date as fallback key.
            exists = False
            if job_url:
                exists = HotJob.objects.filter(job_url=job_url).exists()
            else:
                exists = HotJob.objects.filter(
                    company_name=vd.get('company_name'),
                    position=vd.get('position'),
                    scraped_date=vd.get('scraped_date')
                ).exists()

            if exists:
                skipped.append({'item': item, 'reason': 'duplicate'})
                continue

            # create new record
            job = HotJob.objects.create(
                company_name=vd.get('company_name'),
                company_logo_url=vd.get('company_logo_url', ''),
                position=vd.get('position'),
                job_url=vd.get('job_url', ''),
                scraped_date=vd.get('scraped_date'),
            )
            created.append(JobSerializer(job).data)

        resp = {'created': created, 'skipped': skipped}
        if errors:
            resp['errors'] = errors

        status_code = status.HTTP_201_CREATED if created else status.HTTP_400_BAD_REQUEST
        return Response(resp, status=status_code)


class GetDataView(APIView):
    """GET: list persisted hot jobs (JSON)."""

    def get(self, request):
        qs = HotJob.objects.all().order_by('-created_at')
        serializer = JobSerializer(qs, many=True)
        return Response(serializer.data)
