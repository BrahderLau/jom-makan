from collections import Counter
from django.shortcuts import render
from django.db.models import Prefetch, Count, Avg
from django.http import HttpResponse
from .models import FNB, Review
import ast
from itertools import cycle
from django.db.models import Func, FloatField
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.http import HttpResponse
from collections import Counter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def generate_wordcloud_for_fnb(fnb_id):
    # Fetch all reviews for the given FNB
    reviews = Review.objects.filter(fnb_id=fnb_id).values_list('text', flat=True)
    
    # Ensure each review text is a string and filter out None values
    text = ' '.join([review for review in reviews if review])

    if not text:
        return None
    
    # Define stopwords to exclude
    stopwords = set(STOPWORDS)

    # Generate a word cloud image
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=100, width=600, height=600).generate(text)

    # Save the generated image to a BytesIO object
    image_io = BytesIO()
    wordcloud.to_image().save(image_io, 'PNG')
    image_io.seek(0)

    # Convert image to base64 to embed in HTML
    image_base64 = base64.b64encode(image_io.getvalue()).decode()

    return image_base64

def index(request):

    class Round(Func):
        function = 'ROUND'
        template='%(function)s(%(expressions)s, 2)'
        
    # Prefetch the reviews and their related reviewers
    reviews_prefetch = Prefetch('reviews', queryset=Review.objects.select_related('reviewer'))
    
    # Fetch all FNB ojbects, prefetching related reviews and their reviewers
    fnbs = FNB.objects.prefetch_related(reviews_prefetch).all().annotate(
        average_rating=Round(Avg('reviews__rating')),
        reviews_count=Count('reviews')
    )

    top_5_fnbs = fnbs[:5]

    """
        Paginations Here
    """

    default_page = 1
    page = request.GET.get('page', default_page)

    # Get queryset of FNBs to paginate

    # Paginated FNBs
    fnbs_per_page = 5
    paginator = Paginator(fnbs, fnbs_per_page)

    try:
        fnbs_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fnbs_page = paginator.page(default_page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fnbs_page = paginator.page(paginator.num_pages)

    """
        EDA Functions Here
    """

    # Calculate total reviews and overall average rating across all FNBs
    total_fnbs_count = FNB.objects.count()
    total_reviews_count = Review.objects.count()
    overall_average_rating = Review.objects.aggregate(overall_avg_rating=Avg('rating'))['overall_avg_rating']
    overall_average_rating = "{:.2f}".format(overall_average_rating)

    categories = [
        "Halal Food", "Western Food", "Fast Food", "Vegetarian Food", 
        "Chinese Food", "Indian Food", "Malay Food", "Middle Eastern Food", 
        "Japanese Food", "Korean Food", "Cafe", "Dessert"
    ]
    
    gradients = [
        'bg-gradient-primary', 'bg-gradient-secondary', 'bg-gradient-success',
        'bg-gradient-info', 'bg-gradient-warning', 'bg-gradient-danger',
        'bg-gradient-light', 'bg-gradient-dark'
    ]

    # Calculate the number of FNBs per each category

    category_counter = Counter()

    for fnb in fnbs:
        # Directly update the counter with the categories for this FNB
        category_counter.update(fnb.categories)

    # Convert the counter to a list of (category, count) tuples for easy rendering in the template
    category_counts = list(category_counter.items())
    category_counts = sorted(category_counts, key=lambda x: x[1], reverse=True)

    gradient_cycle = cycle(gradients)

    for fnb in fnbs_page:
        fnb.wordcloud_image = generate_wordcloud_for_fnb(fnb.id)
        fnb.category_gradients = [(category, next(gradient_cycle)) for category in fnb.categories]
    
    # Calculate the number of fnbs for each categories
    return render(request, 'pages/index.html', {
        'fnbs_page': fnbs_page,
        'top_5_fnbs': top_5_fnbs,
        'total_fnbs_count': total_fnbs_count,
        'total_reviews_count': total_reviews_count,
        'overall_average_rating': overall_average_rating,
        'category_counts': category_counts
    })
