# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
# Create your models here.

class AmazonProduct(models.Model):
    asin = models.CharField(db_column='ASIN', primary_key=True, max_length=20)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=60, blank=True, null=True)  # Field name made lowercase.
    sale_price = models.CharField(db_column='SALE_PRICE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    original_price = models.CharField(db_column='ORIGINAL_PRICE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    availability = models.CharField(db_column='AVAILABILITY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=60, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='IMAGE', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'amazon_product'


class AmazonRatings(models.Model):
    asin = models.CharField(db_column='ASIN', primary_key=True, max_length=20)  # Field name made lowercase.
    number_1_star = models.CharField(db_column='1_STAR', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_2_star = models.CharField(db_column='2_STAR', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_3_star = models.CharField(db_column='3_STAR', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_4_star = models.CharField(db_column='4_STAR', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_5_star = models.CharField(db_column='5_STAR', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'amazon_ratings'


class AmazonReviews(models.Model):
    review_id = models.CharField(db_column='REVIEW_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    asin = models.CharField(db_column='ASIN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    header = models.CharField(db_column='HEADER', max_length=80, blank=True, null=True)  # Field name made lowercase.
    text = models.CharField(db_column='TEXT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    rating = models.CharField(db_column='RATING', max_length=20, blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(db_column='AUTHOR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    comment_count = models.CharField(db_column='COMMENT_COUNT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='DATE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    polarity = models.FloatField(db_column='POLARITY', blank=True, null=True)  # Field name made lowercase.
    subjectivity = models.FloatField(db_column='SUBJECTIVITY', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'amazon_reviews'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Query(models.Model):
    qid = models.AutoField(db_column='QID', primary_key=True)  # Field name made lowercase.
    query = models.CharField(db_column='QUERY', max_length=60, blank=True, null=True)  # Field name made lowercase.
    asin = models.CharField(db_column='ASIN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tid = models.CharField(db_column='TID', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'query'

        
    
    

