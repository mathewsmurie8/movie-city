from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from movies.choices import GENRE, MOVIE_TYPES
from movies.models import Movie
from accounts.models import BDSGUser

def index(request):
    listings = Movie.objects.all()
    if not listings:
        messages.error(request, 'There are no movies available at this time. Thank you')

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
        'genre': GENRE,
        'movie_types': MOVIE_TYPES,
    }

    return render(request, 'pages/index.html', context)

def listing(request, listing_id):
  bdsg_user = None
  listing = get_object_or_404(Movie, pk=listing_id)
  if request.user.is_authenticated:
    bdsg_user = BDSGUser.objects.get(user=request.user)


  context = {
    'movie_types': MOVIE_TYPES,
    'genre': GENRE,
    'bdsg_user': bdsg_user,
    'listing': listing
  }

  return render(request, 'listings/listing.html', context)

def about(request):
    context = {}

    return render(request, 'pages/about.html', context)
