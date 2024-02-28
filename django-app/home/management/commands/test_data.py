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

class Command(BaseCommand): 
    help = 'Check data'
  
    def handle(self, *args, **kwargs): 
        fnb = FNB.objects.first()  # Get the first instance for testing
        print(type(fnb.categories))  # Should output: <class 'list'>
        print(fnb.categories)  # This should output the list of categories