from dateutil.parser import parse
from tracemalloc import start
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from movies.choices import MOVIE_TYPES, GENRE
from movies.models import Movie, RentalRequest, RentalRate
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


def search(request):
  queryset_list = Movie.objects.all()
  bdsg_user = None
  if request.user.is_authenticated:
    bdsg_user = BDSGUser.objects.get(user=request.user)

  # Major search fields
  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.annotate(
        search=SearchVector('name'),
          ).filter(search=keywords)

  # Genre
  if 'genre' in request.GET:
    genre = request.GET['genre']
    if genre:
      queryset_list = queryset_list.filter(genre=genre)

  # Movie Type
  if 'movie_type' in request.GET:
    movie_type = request.GET['movie_type']
    if movie_type:
      queryset_list = queryset_list.filter(movie_type=movie_type)

  context = {
    'genre': GENRE,
    'movie_types': MOVIE_TYPES,
    'listings': queryset_list,
    'bdsg_user': bdsg_user,
    'values': request.GET
  }

  return render(request, 'listings/search.html', context)


def get_total_amount(start_date, end_date, movie):
  """Get total amount to rent a movie for a specified period."""
  start_date = parse(start_date).date()
  end_date = parse(end_date).date()
  movie_type = movie.movie_type
  rental_rate = RentalRate.objects.get(movie_type=movie_type)
  total_days = (end_date - start_date).days
  if movie_type == 'REGULAR':
    total_amount = total_days * rental_rate.daily_rate
  elif movie_type == 'CHILDREN':
    total_amount = (total_days * rental_rate.daily_rate) + movie.maximum_age/2
  elif movie_type == 'NEW_RELEASE':
    release_year = movie.year_released.strftime("%Y-%m-%d").split('-')[0]
    total_amount = (total_days * rental_rate.daily_rate) + release_year
  else:
    total_amount = 0
  return total_amount


def rent(request):
  if request.method == 'POST':
    listing_id = request.POST['listing_id']
    movie = Movie.objects.get(id=listing_id)
    user = request.user

    #  Check if user has made inquiry already
    if request.user.is_authenticated:
      user_id = request.user.id
      rental_request_exists = RentalRequest.objects.filter(
        movie=movie, user=user).exists()
      if rental_request_exists:
        messages.error(request, 'You have already made an request for this listing')
        return redirect('/movies/'+listing_id)
      else:
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        total_amount = get_total_amount(start_date, end_date, movie)

        RentalRequest.objects.create(
          movie=movie, user=user, start_date=start_date,
          end_date=end_date, total_amount=total_amount)
        messages.success(request, 'Your request has been successfully created')
        return redirect('/movies/'+listing_id)
