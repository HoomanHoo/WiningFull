# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class WinSearch(models.Model):
    search_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user.WinUser", models.CASCADE)  #
    search_word = models.CharField(max_length=200)
    search_time = models.DateTimeField()

    class Meta:
        # managed = False
        db_table = "win_search"


class WinSearchN(models.Model):
    search_n_id = models.AutoField(primary_key=True)
    search_n_word = models.CharField(max_length=200)
    search_n_time = models.DateTimeField()

    class Meta:
        # managed = False
        db_table = "win_search_n"


class WinRecommend(models.Model):
    recommend_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30)
    recommend_rank_1 = models.IntegerField()
    recommend_rank_2 = models.IntegerField()
    recommend_rank_3 = models.IntegerField()
    recommend_rank_4 = models.IntegerField()
    recommend_rank_5 = models.IntegerField()
    recommend_rank_6 = models.IntegerField()
    recommend_rank_7 = models.IntegerField()
    recommend_rank_8 = models.IntegerField()
    recommend_rank_9 = models.IntegerField()
    recommend_rank_10 = models.IntegerField()
    update_time = models.DateTimeField()

    class Meta:
        # managed = False
        db_table = "win_recommend"
