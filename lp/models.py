from django.db import models
from .relations import SocialMedia


class Book(models.Model):
    """
    A model for handling books released by the learning center.
    """

    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='files')

    objects = models.Manager()

    def __str__(self):
        
        return self.name


class FAQ(models.Model):
    """
    A model for handling frequently asked questions that appear on the main page.
    """

    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=500)

    objects = models.Manager()

    def __str__(self):

        return self.question[50:] + '...' if len(self.question) > 50 else self.question


class IndexInfo(models.Model):
    """
    A model for handling the information that goes to the main and base pages.
    """

    class Meta:

        verbose_name = 'Index information'
        verbose_name_plural = 'Index information'

    brand = models.ImageField(upload_to='images', null=True)
    brand_height = models.PositiveIntegerField(null=True)
    title = models.CharField(max_length=200, null=True)
    product_title = models.CharField(max_length=200)
    product_info = models.TextField()
    company_requisities = models.CharField(max_length=200, null=True)
    footer_motto = models.CharField(max_length=300)
    media = models.ManyToManyField(SocialMedia)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        
        return self.title


class Place(models.Model):
    """
    A model for handling how many places are in total available for a course and how many of them are taken.
    """

    available_places = models.PositiveIntegerField(null=True)
    booked_places = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    def __str__(self):

        return self.available_places
