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
    help = 'Import FNB, Reviewer and Review data'
  
    def handle(self, *args, **kwargs): 

        csv_file_path = '../csv_data/fnb_list_part_7_reviews.csv'

        with open(csv_file_path, newline='') as csvfile:
            
            reader = csv.DictReader(csvfile)
            row_count = 0 

            for row in tqdm(reader, desc="Processing fnb rows..."):

                fnb = None
                reviewer = None
                review = None

                # Parse expiry date
                expiry_date = row.get('Halal Certification Expiry Date')
                if expiry_date:
                    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
                else:
                    expiry_date = None

                # Parse opening hours dictionary
                opening_hours = row.get('Opening Hours')
                if opening_hours:
                    opening_hours = ast.literal_eval(opening_hours)
                else: 
                    opening_hours = {}

                categories = row.get('Category')
                if categories:
                    categories = ast.literal_eval(categories)
                else: 
                    categories = []

                try:

                    fnb = FNB.objects.create(
                        name=row['Name'], 
                        photo=row['Photo'],            
                        categories=categories,
                        opening_hours=opening_hours,
                        area=row['Area'],
                        located_in=row['Located In'],
                        address=row['Address'],
                        phone=row['Phone'],
                        google_map_url=row['Google Map Url'],
                        menu_url=row['Menu Url'],
                        website_url=row['Website Url'],
                        order_url=row['Order Url'],
                        company_brand_name=row['Company Brand Name'],
                        halal_certification_expiry_date=expiry_date,
                        halal_certification_body=row['Halal Certification Body']
                    )

                except Exception as e:

                    print(f'Error importing fnb data for "{row_count}. {row["Name"]}": {e}', file=sys.stderr)

                try:

                    if len(row['Reviews']) == 0:
                        continue

                    review_list = ast.literal_eval(row['Reviews'])

                    for review in tqdm(review_list, desc="Processing reviews..."):

                        try:                      

                            reviewer_info = review['Reviewer']

                            """ 
                            Here we use get_or_create function in Reviewer because it is possible 
                            to have one reviewer to review multiple reivews. Hence, not required to
                            store the same Reviewer data
                            """

                            photos_count = reviewer_info.get('Photos Count')
                            if photos_count is None:
                                photos_count = 0

                            reviewer, created = Reviewer.objects.get_or_create(
                                name=reviewer_info['Name'],
                                defaults={
                                    'reviews_count': reviewer_info['Reviews Count'],
                                    'photos_count': photos_count,
                                    'type': reviewer_info['Type'],
                                    'url': reviewer_info['Url']
                                }
                            )

                        except Exception as e:
                        
                            print(f'Error importing reviewer data for "{row_count}. {row["Name"]}": {e}', file=sys.stderr)

                        try: 
                            """ 
                            Here we use get_or_create function in Review because fnb
                            and reviewer object has already been created. So just link them.
                            """
                            photos = review.get('photos')
                            if photos:
                                photos = ast.literal_eval(photos)
                            else: 
                                photos = []

                            review, created = Review.objects.get_or_create(
                                fnb=fnb,
                                reviewer=reviewer,
                                defaults={
                                    'rating': review['Rating'],
                                    'text': review['Text'],
                                    'photos': photos
                                }
                            )

                        except Exception as e:
                        
                            print(f'Error importing review data for "{row_count}. {row["Name"]}": {e}', file=sys.stderr)

                except Exception as e:
                    
                    print(f'Error importing reviewer or review data for "{row_count}. {row["Name"]}": {e}', file=sys.stderr)

                row_count += 1

# if __name__ == '__main__':

#     import_fnb_data(csv_file_path)
