from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class GovtJob(models.Model):
    """Government Job record from bdgovtjob.net scraper.
    
    Fields correspond to the bdgovtjob scraper output:
    - job_title: Full job circular title
    - job_url: Link to the job circular
    - vacancies: Number of positions available
    - deadline: Application deadline
    - posted_date: When the job was posted
    - scraped_at: When the data was scraped
    """
    
    job_title = models.TextField(blank=True, null=True)
    job_url = models.URLField(max_length=500, blank=True, null=True, unique=True)
    vacancies = models.CharField(max_length=100, blank=True, null=True)
    deadline = models.CharField(max_length=200, blank=True, null=True)
    posted_date = models.CharField(max_length=100, blank=True, null=True)
    scraped_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Government Job'
        verbose_name_plural = 'Government Jobs'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['job_url']),
        ]
    
    def __str__(self):
        return f"{self.job_title or 'Unknown'} - {self.vacancies or 'N/A'} positions"
    
    def clean_url(self, value):
        """Normalize URL-like fields: treat empty, whitespace or 'N/A' as None."""
        if value is None:
            return None
        if isinstance(value, str):
            v = value.strip()
            if not v or v.upper() == 'N/A':
                return None
            try:
                URLValidator()(v)
            except ValidationError:
                return v
            return v
        return value
    
    def save(self, *args, **kwargs):
        # Normalize job_title
        if isinstance(self.job_title, str):
            self.job_title = self.job_title.strip() or None
        
        # Normalize job_url
        self.job_url = self.clean_url(self.job_url)
        
        # Normalize vacancies
        if isinstance(self.vacancies, str):
            v = self.vacancies.strip()
            self.vacancies = v if v and v.upper() != 'N/A' else None
        
        # Normalize deadline
        if isinstance(self.deadline, str):
            d = self.deadline.strip()
            self.deadline = d if d and d.upper() != 'N/A' else None
        
        # Normalize posted_date
        if isinstance(self.posted_date, str):
            p = self.posted_date.strip()
            self.posted_date = p if p and p.upper() != 'N/A' else None
        
        # Parse scraped_at if it's a string
        if isinstance(self.scraped_at, str):
            try:
                from datetime import datetime
                parsed = datetime.strptime(self.scraped_at, '%Y-%m-%d %H:%M:%S')
                self.scraped_at = timezone.make_aware(parsed, timezone.get_current_timezone())
            except Exception:
                try:
                    parsed = timezone.datetime.fromisoformat(self.scraped_at)
                    if timezone.is_naive(parsed):
                        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
                    self.scraped_at = parsed
                except Exception:
                    self.scraped_at = None
        
        super().save(*args, **kwargs)

