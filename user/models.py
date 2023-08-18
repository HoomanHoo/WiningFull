from django.db import models


class WinUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=30)
    user_grade = models.ForeignKey(
        "WinUserGrade", models.CASCADE, db_column="user_grade", default=1
    )
    user_passwd = models.CharField(max_length=30)
    user_name = models.CharField(max_length=20)
    user_email = models.CharField(max_length=50)
    user_tel = models.CharField(max_length=20)
    user_reg_date = models.DateTimeField()
    user_point = models.PositiveIntegerField()
    user_profile_img = models.ImageField(
        upload_to="profile/", blank=True, max_length=300, default=""
    )

    class Meta:
        # managed = False
        db_table = "win_user"


class WinUserAccount(models.Model):
    user_account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("WinUser", models.CASCADE, db_column="user_id", default="")
    user_account_default = models.IntegerField(default=1)
    user_account1 = models.CharField(default="", max_length=80, blank=True)
    user_account2 = models.CharField(default="", max_length=80, blank=True)
    user_account3 = models.CharField(default="", max_length=80, blank=True)

    class Meta:
        db_table = "win_user_account"
        managed = True


class WinUserFavorite(models.Model):
    fav_user_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(WinUser, models.CASCADE)  #
    fav_wine_color = models.IntegerField()
    fav_alc = models.IntegerField()
    fav_numbwith = models.IntegerField()
    fav_sweet = models.IntegerField()
    fav_bitter = models.IntegerField()
    fav_sour = models.IntegerField()
    fav_season = models.IntegerField()
    fav_food = models.IntegerField()
    fav_first_priority = models.IntegerField()
    fav_second_priority = models.IntegerField()
    fav_third_priority = models.IntegerField()

    class Meta:
        # managed = False
        db_table = "win_user_favorite"


class WinUserGrade(models.Model):
    user_grade = models.IntegerField(primary_key=True)
    user_grade_name = models.CharField(unique=True, max_length=30)

    class Meta:
        # managed = False
        db_table = "win_user_grade"


class WinPointHis(models.Model):
    point_his_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("WinUser", models.CASCADE)  #
    point_reg = models.DateTimeField()
    point_add = models.IntegerField()

    class Meta:
        # managed = False
        db_table = "win_point_his"


class WinReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("WinUser", models.CASCADE)  #
    sell = models.ForeignKey("store.WinSell", models.CASCADE, default="")  #
    review_content = models.CharField(max_length=500)
    review_score = models.DecimalField(max_digits=2, decimal_places=1)
    review_reg_time = models.DateTimeField()

    class Meta:
        # managed = False
        db_table = "win_review"
