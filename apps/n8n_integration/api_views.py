from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q
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
    """GET: list persisted hot jobs with optional filters via query params."""

    def get(self, request):
        qs = HotJob.objects.all()
        
        # Filter by days (last N days)
        days = request.query_params.get('days')
        if days:
            try:
                days_int = int(days)
                date_from = timezone.now() - timedelta(days=days_int)
                qs = qs.filter(created_at__gte=date_from)
            except ValueError:
                pass
        
        # Filter by date range
        start_date = request.query_params.get('start')
        if start_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                start_aware = timezone.make_aware(start, timezone.get_current_timezone())
                qs = qs.filter(created_at__gte=start_aware)
            except ValueError:
                pass
        
        end_date = request.query_params.get('end')
        if end_date:
            try:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                end_aware = timezone.make_aware(end, timezone.get_current_timezone())
                # Add 1 day to include the end date
                end_aware = end_aware + timedelta(days=1)
                qs = qs.filter(created_at__lt=end_aware)
            except ValueError:
                pass
        
        # Filter by company name (case-insensitive partial match)
        company = request.query_params.get('company')
        if company:
            qs = qs.filter(company_name__icontains=company)
        
        # Filter by position (case-insensitive partial match)
        position = request.query_params.get('position')
        if position:
            qs = qs.filter(position__icontains=position)
        
        qs = qs.order_by('-created_at')
        serializer = JobSerializer(qs, many=True)
        
        return Response({
            'filters': {
                'days': days,
                'start_date': start_date,
                'end_date': end_date,
                'company': company,
                'position': position,
            },
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetTodayDataView(APIView):
    """GET: Jobs scraped today"""
    
    def get(self, request):
        today = timezone.now().date()
        qs = HotJob.objects.filter(
            created_at__date=today
        ).order_by('-created_at')
        serializer = JobSerializer(qs, many=True)
        return Response({
            'date': str(today),
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetYesterdayDataView(APIView):
    """GET: Jobs scraped yesterday"""
    
    def get(self, request):
        yesterday = timezone.now().date() - timedelta(days=1)
        qs = HotJob.objects.filter(
            created_at__date=yesterday
        ).order_by('-created_at')
        serializer = JobSerializer(qs, many=True)
        return Response({
            'date': str(yesterday),
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetWeekDataView(APIView):
    """GET: Jobs scraped in the last 7 days"""
    
    def get(self, request):
        week_ago = timezone.now() - timedelta(days=7)
        qs = HotJob.objects.filter(
            created_at__gte=week_ago
        ).order_by('-created_at')
        serializer = JobSerializer(qs, many=True)
        return Response({
            'period': 'last_7_days',
            'from': str(week_ago.date()),
            'to': str(timezone.now().date()),
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetMonthDataView(APIView):
    """GET: Jobs scraped this month"""
    
    def get(self, request):
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        qs = HotJob.objects.filter(
            created_at__gte=month_start
        ).order_by('-created_at')
        serializer = JobSerializer(qs, many=True)
        return Response({
            'period': 'current_month',
            'month': now.strftime('%B %Y'),
            'from': str(month_start.date()),
            'to': str(now.date()),
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetDateDataView(APIView):
    """GET: Jobs scraped on specific date"""
    
    def get(self, request, date_str):
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD (e.g., 2025-11-03)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        qs = HotJob.objects.filter(
            created_at__date=target_date
        ).order_by('-created_at')
        serializer = JobSerializer(qs, many=True)
        return Response({
            'date': str(target_date),
            'count': qs.count(),
            'jobs': serializer.data
        })
