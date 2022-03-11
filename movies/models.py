import os
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from movies.choices import MOVIE_TYPES, GENRE, REQUEST_STATUS


class RentalRate(models.Model):
    """Holds movie rental rates based on movie type."""
    movie_type = models.CharField(max_length=255, choices=MOVIE_TYPES)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)


class Movie(models.Model):
    """Holds all movie records."""
    name = models.CharField(max_length=255)
    movie_type = models.CharField(max_length=255, choices=MOVIE_TYPES)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    genre = models.CharField(max_length=255, choices=GENRE)
    popularity = models.DecimalField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        max_digits=4, decimal_places=2)
    maximum_age = models.IntegerField(null=True, blank=True)
    year_released = models.DateField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, max_length=255)
    updated = models.DateTimeField(default=timezone.now, max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        """Str representation for the data."""
        return self.name

    def validate_year_of_release_set_for_new_releases(self):
        """Validate that the year_released is set for new release."""
        if not self.year_released and self.movie_type == 'NEW_RELEASE':
            raise ValidationError(
                'The year of release should be specified for a NEW_RELEASE')

    def validate_maximum_age_is_set_for_childrens_movies(self):
        """Validate any children's movie has a maximum age limit."""
        if self.movie_type == 'CHILDREN' and not self.maximum_age:
            raise ValidationError(
                'A childrens movie must have a maximum age specified.')

    def validate_name_is_unique(self):
        """Error handling when a user provides the same name."""
        name_exists = self.__class__.objects.filter(
            name=self.name).exclude(pk=self.pk)
        if self.name and name_exists.exists():
            raise ValidationError(
                'A movie with this name already exists.' +
                'Please provide another name')

    def clean(self, *args, **kwargs):
        """Override clean to call custom validators."""
        self.validate_year_of_release_set_for_new_releases()
        self.validate_name_is_unique()
        self.validate_maximum_age_is_set_for_childrens_movies()
        super().clean(*args, **kwargs)


class RentalRequest(models.Model):
    """Holds all the rental requests from users."""
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(
        default='PENDING', max_length=255, choices=REQUEST_STATUS)

    def save(self, *args, **kwargs):
        """Override save method."""
        self.full_clean(exclude=None)
        super(RentalRequest, self).save(*args, **kwargs)
