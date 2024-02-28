import csv
import sys
import os
import json
import ast
from tqdm import tqdm
from datetime import datetime
from home.models import FNB, Reviewer, Review
from django.core.management.base import BaseCommand

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

"""
In the get_or_create method, defaults is used to provide initial values for model fields for a new object. 
These values are only used if Django needs to create a new object.
If the object is fetched, defaults does not update the object. 

Reference: https://www.letscodemore.com/blog/django-get-or-create/
"""

class Command(BaseCommand): 
    help = 'Remove all data'
  
    def handle(self, *args, **kwargs): 

        if FNB.objects.exists():
            print("Data exists in FNB. Removing...")
            FNB.objects.all().delete()
            print("FNB data removed.")
        else:
            print("No data found in FNB.")

        if Reviewer.objects.exists():
            print("Data exists in Reviewer. Removing...")
            Reviewer.objects.all().delete()
            print("Reviewer data removed.")
        else:
            print("No data found in Reviewer.")

        if Review.objects.exists():
            print("Data exists in Review. Removing...")
            Review.objects.all().delete()
            print("Review data removed.")
        else:
            print("No data found in Review.")

       