from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class HotJob(models.Model):
    """Job record for Hot Jobs.

    Fields are permissive to accommodate CSV rows with missing/placeholder
    values (empty strings, whitespace, or 'N/A'). The model normalizes
    these values to None where appropriate.
    """

    company_name = models.TextField(blank=True, null=True)
    company_logo_url = models.URLField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    job_url = models.URLField(blank=True, null=True)
    scraped_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name or 'Unknown'} - {self.position or 'Unknown'}"

    def clean_url(self, value):
        """Normalize URL-like fields: treat empty, whitespace or 'N/A' as None.

        If a non-empty value is provided, attempt a basic URL validation and
        return the original string (no further normalization).
        """
        if value is None:
            return None
        if isinstance(value, str):
            v = value.strip()
            if not v or v.upper() == 'N/A':
                return None
            # basic validation (will raise on invalid URL)
            try:
                URLValidator()(v)
            except ValidationError:
                # keep the raw value — downstream consumers can handle it
                return v
            return v
        return value

    def save(self, *args, **kwargs):
        # Normalize company_name and position: strip and set None for empty
        if isinstance(self.company_name, str):
            self.company_name = self.company_name.strip() or None
        if isinstance(self.position, str):
            # collapse multiple spaces and strip
            cleaned = ' '.join(self.position.split())
            self.position = cleaned or None

        # Normalize URL fields
        self.company_logo_url = self.clean_url(self.company_logo_url)
        self.job_url = self.clean_url(self.job_url)

        # If scraped_date is a string, try to parse it (best-effort)
        if isinstance(self.scraped_date, str):
            try:
                # use django's timezone parsing
                parsed = timezone.datetime.fromisoformat(self.scraped_date)
                # make timezone-aware using current timezone if naive
                if timezone.is_naive(parsed):
                    parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
                self.scraped_date = parsed
            except Exception:
                # leave as-is (DB will reject non-datetime) — fallback to None
                try:
                    self.scraped_date = timezone.datetime.strptime(self.scraped_date, '%Y-%m-%d %H:%M:%S')
                    self.scraped_date = timezone.make_aware(self.scraped_date, timezone.get_current_timezone())
                except Exception:
                    self.scraped_date = None

        super().save(*args, **kwargs)
