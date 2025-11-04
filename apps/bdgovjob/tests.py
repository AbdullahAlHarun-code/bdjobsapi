from django.test import TestCase
from django.utils import timezone
from .models import GovtJob


class GovtJobModelTest(TestCase):
    """Test cases for GovtJob model"""
    
    def test_create_govt_job(self):
        """Test creating a government job"""
        job = GovtJob.objects.create(
            job_title="Planning Division Job Circular 2025",
            job_url="https://bdgovtjob.net/planning-division-job-circular/",
            vacancies="65",
            deadline="25 November 2025 at 5:00 PM",
            posted_date="3 November, 2025",
            scraped_at=timezone.now()
        )
        self.assertEqual(job.job_title, "Planning Division Job Circular 2025")
        self.assertEqual(job.vacancies, "65")
        self.assertIsNotNone(job.created_at)
    
    def test_job_url_unique(self):
        """Test that job_url is unique"""
        GovtJob.objects.create(
            job_title="Test Job 1",
            job_url="https://example.com/job1/",
            vacancies="10"
        )
        
        # Try to create another with same URL - should raise error
        with self.assertRaises(Exception):
            GovtJob.objects.create(
                job_title="Test Job 2",
                job_url="https://example.com/job1/",
                vacancies="20"
            )
    
    def test_normalize_na_values(self):
        """Test that N/A values are normalized to None"""
        job = GovtJob.objects.create(
            job_title="Test Job",
            job_url="https://example.com/test/",
            vacancies="N/A",
            deadline="N/A",
            posted_date="N/A"
        )
        # After save, N/A should be None
        job.refresh_from_db()
        self.assertIsNone(job.vacancies)
        self.assertIsNone(job.deadline)
        self.assertIsNone(job.posted_date)

