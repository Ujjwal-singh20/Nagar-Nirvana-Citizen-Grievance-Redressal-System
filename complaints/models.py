from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    citizen = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complaints'
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    video = models.FileField(upload_to='complaints/', blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Submitted'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    attachment = models.FileField(upload_to='complaints/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.citizen.username}"


class ComplaintUpdate(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Complaint.STATUS_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Update on {self.complaint.title} by {self.updated_by.username}"

class Feedback(models.Model):
    RESOLUTION_CHOICES = [
        ('confirmed', 'Issue resolved'),
        ('pending', 'Issue still pending'),
    ]

    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE)
    resolution_status = models.CharField(max_length=20, choices=RESOLUTION_CHOICES)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback for {self.complaint.title}"
