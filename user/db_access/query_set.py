from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from user.models import WinUser, WinUserFavorite


@transaction.atomic()
def insert_user_info(user_info, is_store: bool = False, user_favorite_info=None):
    user_info.save()
    if is_store is False:
        user_favorite_info.save()


def check_id(user_id) -> dict:
    """
    회원정보가 존재하면 WinUserObject와 result = 1을 리턴
    회원정보가 존재하지 않으면 None과 result = 0을 리턴
    리턴 타입은 dictionary, {"result": result, "user_info": "WinUserObject" or None}
    """
    try:
        user_info = WinUser.objects.get(user_id=user_id)
        result = 1
    except ObjectDoesNotExist:
        user_info = None
        result = 0

    return {"result": result, "user_info": user_info}


def check_login(user_id: str, is_kakao: bool, user_passwd: str = None) -> int:
    """
    return 1 = 비밀번호 일치, 회원 등급 일반 유저 이상
    return -1 = 비밀번호 일치, 회원 등급 탈퇴 회원
    return -2 = 비밀번호 불일치
    return -3 = 아이디 불일치
    """

    try:
        user_info = WinUser.objects.get(user_id=user_id)
        user_grade = user_info.user_grade

        if is_kakao:
            if user_grade != -1:
                return 1

            else:
                return -1

        else:
            if user_passwd == user_info.user_passwd:
                if user_grade != -1:
                    return 1

                else:
                    return -1

            else:
                return -2
    except ObjectDoesNotExist:
        return -3


def get_favorite_info(user_id):
    try:
        favorite_info = WinUserFavorite.objects.get(user_id=user_id)

    except ObjectDoesNotExist:
        favorite_info = None

    return favorite_info
