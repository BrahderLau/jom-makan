from django.db import models
from datetime import date

# Create your models here.
class FNB(models.Model):
    # Basic Information
    name = models.CharField(max_length=200)
    photo = models.URLField(null=True, blank=True)
    categories = models.JSONField(default=list, blank=True)
    opening_hours = models.JSONField(default=dict, blank=True)
    area = models.CharField(max_length=50)
    located_in = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=17, null=True, blank=True)

    # URLs
    google_map_url = models.URLField(null=True, blank=True) 
    menu_url = models.URLField(null=True, blank=True)  
    website_url = models.URLField(null=True, blank=True)
    order_url = models.URLField(null=True, blank=True)

    # Company and Halal Certification information
    company_brand_name = models.CharField(max_length=200, null=True, blank=True)
    halal_certification_expiry_date = models.DateField(null=True, blank=True) 
    halal_certification_body = models.CharField(max_length=200, null=True, blank=True) 

    def __str__(self):
        return self.name

    def is_halal_expired(self):
        return date.today() > self.halal_certification_expiry_date


class Reviewer(models.Model):
    name = models.CharField(max_length=100)
    reviews_count = models.IntegerField(default=0)
    photos_count = models.IntegerField(default=0)
    type = models.CharField(max_length=20, null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.name


class Review(models.Model):
    fnb = models.ForeignKey('FNB', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey('Reviewer', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    text = models.TextField(null=True, blank=True)
    photos = models.JSONField(default=list, blank=True) 

    def __str__(self):
        return self.text if self.text else "N/A"
