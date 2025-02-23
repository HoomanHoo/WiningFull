from django.contrib import admin
from user.models import (
    WinUser,
    WinUserAccount,
    WinUserFavorite,
    WinUserGrade,
    WinPointHis,
)


class WinUserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "user_grade",
        "user_passwd",
        "user_name",
        "user_email",
        "user_tel",
        "user_reg_date",
        "user_point",
        "user_profile_img",
    )


admin.site.register(WinUser, WinUserAdmin)


class WinUserAccountAdmin(admin.ModelAdmin):
    list_display = (
        "user_account_id",
        "user_id",
        "user_account_default",
        "user_account1",
        "user_account2",
        "user_account3",
    )


admin.site.register(WinUserAccount, WinUserAccountAdmin)


class WinUserFavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "fav_user_id",
        "user_id",
        "fav_wine_color",
        "fav_alc",
        "fav_numbwith",
        "fav_sweet",
        "fav_bitter",
        "fav_sour",
        "fav_season",
        "fav_food",
    )


admin.site.register(WinUserFavorite, WinUserFavoriteAdmin)


class WinUserGradeAdmin(admin.ModelAdmin):
    list_display = ("user_grade", "user_grade_name")


admin.site.register(WinUserGrade, WinUserGradeAdmin)


class WinPointHisAdmin(admin.ModelAdmin):
    list_display = ("point_his_id", "user_id", "point_reg", "point_add")


admin.site.register(WinPointHis, WinPointHisAdmin)
