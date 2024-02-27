from collections import Counter
from django.shortcuts import render
from django.db.models import Prefetch, Count, Avg
from django.http import HttpResponse
from .models import FNB, Review
import ast

# Create your views here.

def index(request):

    # Prefetch the reviews and their related reviewers
    reviews_prefetch = Prefetch('reviews', queryset=Review.objects.select_related('reviewer'))
    # Fetch top 5 FNB objects, prefetching related reviews and their reviewers
    fnbs = FNB.objects.prefetch_related(reviews_prefetch).all()
    top_5_fnbs = FNB.objects.prefetch_related(reviews_prefetch).all()[:5]

    """
        EDA Functions Here
    """

    # Calculate total reviews and overall average rating across all FNBs
    total_reviews_count = Review.objects.count()
    overall_average_rating = Review.objects.aggregate(overall_avg_rating=Avg('rating'))['overall_avg_rating']
    overall_average_rating = "{:.2f}".format(overall_average_rating)

    # Calculate the number of fnbs for each categories


    return render(request, 'pages/index.html', {
        'top_5_fnbs': top_5_fnbs,
        'total_reviews_count': total_reviews_count,
        'overall_average_rating': overall_average_rating,
        'category_names': 'test',
        'category_counts': 'tes'
    })