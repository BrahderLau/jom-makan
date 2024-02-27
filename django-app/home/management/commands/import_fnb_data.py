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
    help = 'Displays fnb list'
  
    def handle(self, *args, **kwargs): 

        csv_file_path = '../csv_data/fnb_list_part_7_reviews.csv'

        # if FNB.objects.exists():
        #     print("Data exists in FNB. Removing...")
        #     FNB.objects.all().delete()
        #     print("FNB data removed.")
        # else:
        #     print("No data found in FNB.")

        # if Reviewer.objects.exists():
        #     print("Data exists in Reviewer. Removing...")
        #     Reviewer.objects.all().delete()
        #     print("Reviewer data removed.")
        # else:
        #     print("No data found in Reviewer.")

        # if Review.objects.exists():
        #     print("Data exists in Review. Removing...")
        #     Review.objects.all().delete()
        #     print("Review data removed.")
        # else:
        #     print("No data found in Review.")

        with open(csv_file_path, newline='') as csvfile:
            
            reader = csv.DictReader(csvfile)
            row_count = 0 

            for row in tqdm(reader, desc="Processing fnb rows..."):

                fnb = None
                reviewer = None
                review = None

                # Parse date fields
                expiry_date = row.get('Halal Certification Expiry Date')
                if expiry_date:
                    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
                else:
                    expiry_date = None

                try:

                    fnb = FNB.objects.create(
                        name=row['Name'],
                        categories=row['Category'],
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
                            review, created = Review.objects.get_or_create(
                                fnb=fnb,
                                reviewer=reviewer,
                                defaults={
                                    'rating': review['Rating'],
                                    'text': review['Text'],
                                    'photos': review['Photos']
                                }
                            )

                        except Exception as e:
                        
                            print(f'Error importing review data for "{row_count}. {row["Name"]}": {e}', file=sys.stderr)

                except Exception as e:
                    
                    print(f'Error importing reviewer or review data for "{row_count}. {row["Name"]}": {e}', file=sys.stderr)

                row_count += 1

# if __name__ == '__main__':

#     import_fnb_data(csv_file_path)
