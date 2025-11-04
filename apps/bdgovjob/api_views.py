from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q
from .models import GovtJob
from .serializers import GovtJobSerializer


class SendDataView(APIView):
    """POST: accept single or list of government jobs and persist them."""
    
    def post(self, request):
        data = request.data
        payloads = data if isinstance(data, list) else [data]
        
        created = []
        updated = []
        errors = []
        skipped = []
        
        for item in payloads:
            serializer = GovtJobSerializer(data=item)
            if not serializer.is_valid():
                errors.append({'item': item, 'errors': serializer.errors})
                continue
            
            vd = serializer.validated_data
            job_url = (vd.get('job_url') or '').strip()
            
            # Deduplication by job_url (primary key)
            if job_url:
                existing = GovtJob.objects.filter(job_url=job_url).first()
                if existing:
                    # Update existing record
                    for key, value in vd.items():
                        setattr(existing, key, value)
                    existing.save()
                    updated.append(GovtJobSerializer(existing).data)
                    continue
            
            # Create new record
            try:
                job = GovtJob.objects.create(**vd)
                created.append(GovtJobSerializer(job).data)
            except Exception as e:
                errors.append({'item': item, 'error': str(e)})
        
        resp = {
            'created': created,
            'updated': updated,
            'skipped': skipped,
            'total_created': len(created),
            'total_updated': len(updated),
            'total_errors': len(errors),
        }
        
        if errors:
            resp['errors'] = errors
        
        status_code = status.HTTP_201_CREATED if created else (
            status.HTTP_200_OK if updated else status.HTTP_400_BAD_REQUEST
        )
        return Response(resp, status=status_code)


class GetDataView(APIView):
    """GET: list persisted government jobs with optional filters via query params."""
    
    def get(self, request):
        qs = GovtJob.objects.all()
        
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
                end_aware = end_aware + timedelta(days=1)
                qs = qs.filter(created_at__lt=end_aware)
            except ValueError:
                pass
        
        # Filter by job title (case-insensitive partial match)
        title = request.query_params.get('title')
        if title:
            qs = qs.filter(job_title__icontains=title)
        
        # Filter by vacancies
        vacancies = request.query_params.get('vacancies')
        if vacancies:
            qs = qs.filter(vacancies__icontains=vacancies)
        
        # Filter by deadline (partial match)
        deadline = request.query_params.get('deadline')
        if deadline:
            qs = qs.filter(deadline__icontains=deadline)
        
        qs = qs.order_by('-created_at')
        serializer = GovtJobSerializer(qs, many=True)
        
        return Response({
            'filters': {
                'days': days,
                'start_date': start_date,
                'end_date': end_date,
                'title': title,
                'vacancies': vacancies,
                'deadline': deadline,
            },
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetTodayDataView(APIView):
    """GET: Government jobs scraped today"""
    
    def get(self, request):
        today = timezone.now().date()
        qs = GovtJob.objects.filter(
            created_at__date=today
        ).order_by('-created_at')
        serializer = GovtJobSerializer(qs, many=True)
        return Response({
            'date': str(today),
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetYesterdayDataView(APIView):
    """GET: Government jobs scraped yesterday"""
    
    def get(self, request):
        yesterday = timezone.now().date() - timedelta(days=1)
        qs = GovtJob.objects.filter(
            created_at__date=yesterday
        ).order_by('-created_at')
        serializer = GovtJobSerializer(qs, many=True)
        return Response({
            'date': str(yesterday),
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetWeekDataView(APIView):
    """GET: Government jobs scraped in the last 7 days"""
    
    def get(self, request):
        week_ago = timezone.now() - timedelta(days=7)
        qs = GovtJob.objects.filter(
            created_at__gte=week_ago
        ).order_by('-created_at')
        serializer = GovtJobSerializer(qs, many=True)
        return Response({
            'period': 'last_7_days',
            'from': str(week_ago.date()),
            'to': str(timezone.now().date()),
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetMonthDataView(APIView):
    """GET: Government jobs scraped this month"""
    
    def get(self, request):
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        qs = GovtJob.objects.filter(
            created_at__gte=month_start
        ).order_by('-created_at')
        serializer = GovtJobSerializer(qs, many=True)
        return Response({
            'period': 'current_month',
            'month': now.strftime('%B %Y'),
            'from': str(month_start.date()),
            'to': str(now.date()),
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetDateDataView(APIView):
    """GET: Government jobs scraped on specific date"""
    
    def get(self, request, date_str):
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD (e.g., 2025-11-03)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        qs = GovtJob.objects.filter(
            created_at__date=target_date
        ).order_by('-created_at')
        serializer = GovtJobSerializer(qs, many=True)
        return Response({
            'date': str(target_date),
            'count': qs.count(),
            'jobs': serializer.data
        })


class GetStatsView(APIView):
    """GET: Statistics about government jobs"""
    
    def get(self, request):
        total_jobs = GovtJob.objects.count()
        today = timezone.now().date()
        
        # Count jobs by time period
        today_count = GovtJob.objects.filter(created_at__date=today).count()
        week_count = GovtJob.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        month_count = GovtJob.objects.filter(
            created_at__month=today.month,
            created_at__year=today.year
        ).count()
        
        # Count jobs with vacancies
        with_vacancies = GovtJob.objects.exclude(
            Q(vacancies__isnull=True) | Q(vacancies='') | Q(vacancies__iexact='N/A')
        ).count()
        
        # Count jobs with deadlines
        with_deadlines = GovtJob.objects.exclude(
            Q(deadline__isnull=True) | Q(deadline='') | Q(deadline__iexact='N/A')
        ).count()
        
        return Response({
            'total_jobs': total_jobs,
            'today': today_count,
            'this_week': week_count,
            'this_month': month_count,
            'with_vacancies': with_vacancies,
            'with_deadlines': with_deadlines,
            'last_updated': GovtJob.objects.order_by('-created_at').first().created_at if total_jobs > 0 else None
        })

