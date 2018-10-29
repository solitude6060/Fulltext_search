# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=30, blank=True, null=True)
    sentence = models.TextField(blank=True, null=True)
    style = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word'

class Word_frequency(models.Model):
    word = models.CharField(max_length=100, blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=100, blank=True, null=True)
    file_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word_frequency'
