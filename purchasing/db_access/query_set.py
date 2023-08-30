from django.db import transaction
from django.db.models.query import QuerySet
from django.db.models import F, Q
from django.db.models import CharField, Value as V
from django.db.models.functions import (
    ExtractYear,
    ExtractMonth,
    ExtractDay,
    ExtractHour,
    ExtractMinute,
    Concat,
)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from store.models import WinSell, WinRevenue
from user.models import WinReview, WinUser
from purchasing.models import (
    WinPurchase,
    WinPurchaseDetail,
    WinCart,
    WinCartDetail,
    WinReceiveCode,
)


def insert_purchase(result: dict) -> list:
    """
    purchaseUseCase 클래스의 calc() 함수의 연산 결과를 매개변수로 하여 Django ORM을 통해 DB에 구매 목록과 정보를 저장하는 함수이다.
    """

    user_id = result.get("user")
    purchase_time = result.get("current_time")
    purchase_number = result.get("quantity_all")
    purchase_price = result.get("price_all")
    sell_ids = result.get("product_infos")
    purchase_det_numbers = result.get("quantity_per_ones")
    purchase_det_prices = result.get("price_per_ones")
    user_point = result.get("user_point")
    cart_id = result.get("cart_info", None)

    purchase_detail_infos = []
    revenues = []
    purchase_infos = []

    purchase_info = WinPurchase(
        user_id=user_id,
        purchase_time=purchase_time,
        purchase_number=purchase_number,
        purchase_price=purchase_price,
    )
    purchase_info.save()
    purchase_id = purchase_info.purchase_id
    purchase_infos.append(purchase_id)

    for idx, sell_id in enumerate(sell_ids):
        purchase_detail_info = WinPurchaseDetail(
            purchase_id=purchase_id,
            sell_id=sell_id,
            purchase_det_number=purchase_det_numbers[idx],
            purchase_det_price=purchase_det_prices[idx],
            purchase_det_state=1,
        )
        purchase_detail_infos.append(purchase_detail_info)
    WinPurchaseDetail.objects.bulk_create(purchase_detail_infos)

    purchase_detail_ids = WinPurchaseDetail.objects.filter(
        purchase_id=purchase_id
    ).values_list("purchase_detail_id")
    purchase_infos.append(purchase_detail_ids)

    update_point = WinUser.objects.get(user_id=user_id)
    update_point.user_point = user_point
    update_point.save()

    store_ids = list(
        WinSell.objects.filter(sell_id__in=sell_ids).values_list("store_id", flat=True)
    )

    for idx, store_id in enumerate(store_ids):
        revenue = WinRevenue(
            store_id=store_id,
            revenue_value=purchase_det_prices[idx],
            revenue_date=purchase_time,
        )
        revenues.append(revenue)
    WinRevenue.objects.bulk_create(revenues)

    if cart_id is not None:
        update_cart_info = WinCart.objects.get(cart_id=cart_id)
        update_cart_info.cart_state = -1
        update_cart_info.save()

    return purchase_infos


@transaction.atomic
def add_cart_info(user_id: str, sell_id: str, quantity: int, current_time: str) -> int:
    cart_id = get_cart_id(user_id)

    if cart_id is None or cart_id == 0:
        cart_info = WinCart(
            user_id=user_id,
            cart_time=current_time,
            cart_state=1,
        )
        cart_info.save()
        cart_id = cart_info.cart_id

    try:
        cart_detail_info = WinCartDetail.objects.get(
            Q(sell_id=sell_id), Q(cart_id=cart_id)
        )
        cart_detail_info.cart_det_qnty += quantity
        cart_detail_info.save()

    except ObjectDoesNotExist as ex:
        print(ex)
        cart_detail_info = WinCartDetail(
            sell_id=sell_id, cart_id=cart_id, cart_det_qnty=quantity
        )
        cart_detail_info.save()

    return cart_id


def insert_enc_receive_codes(
    enc_receive_codes: list, purchase_detail_ids: list
) -> None:
    db_data = []

    for idx, purchase_detail_id in enumerate(purchase_detail_ids):
        queryset = WinReceiveCode(
            purchase_detail_id=purchase_detail_id[0],
            receive_code=enc_receive_codes[idx],
        )
        db_data.append(queryset)
    WinReceiveCode.objects.bulk_create(db_data)


def delete_detail_cart_info(cart_det_id: str) -> tuple:
    detail_cart = WinCartDetail.objects.get(cart_det_id=cart_det_id)
    result = detail_cart.delete()
    return result


def get_user_info(user_id: str):
    user_info = WinUser.objects.get(user_id=user_id)
    return user_info


def get_cart_id(user_id: str) -> str or None:
    """
    user_id가 존재하고 cart_state가 1이면 (활성화 상태) cart_id를 반환한다
    user_id가 존재하지 않거나 cart_state가 1인 cart_id가 없으면 cart_id = -1을 반환한다
    """

    cart_info = WinCart.objects.filter(user_id=user_id, cart_state=1).values("cart_id")
    if cart_info.count() == 0:
        cart_id = 0
    else:
        cart_id = cart_info[0].get("cart_id")
    return cart_id


def get_cart_state(cart_id):
    cart_state = WinCart.objects.filter(cart_id=cart_id).values("cart_state")

    if cart_state.count() == 0:
        cart_state = -1
    else:
        cart_state = cart_state[0].get("cart_state")
    return cart_state


def get_cart_detail_infos(cart_id: str) -> QuerySet:
    cart_detail_infos = WinCartDetail.objects.filter(cart_id=cart_id)
    return cart_detail_infos


def get_cart_list_page_info(cart_id: str) -> QuerySet:
    """
    SELECT `win_wine`.`wine_image`,
       `win_wine`.`wine_name`,
       `win_cart_detail`.`sell_id`,
       `win_sell`.`sell_price`,
       `win_cart_detail`.`cart_det_qnty`,
       (`win_sell`.`sell_price` * `win_cart_detail`.`cart_det_qnty`) AS `purchase_price`
       `win_cart_detail`.`cart_det_id`
    FROM `win_cart_detail`
    INNER JOIN `win_sell`
    ON (`win_cart_detail`.`sell_id` = `win_sell`.`sell_id`)
    INNER JOIN `win_wine`
    ON (`win_sell`.`wine_id` = `win_wine`.`wine_id`)
    WHERE `win_cart_detail`.`cart_id` = cart_id
    """

    info = (
        WinCartDetail.objects.filter(cart_id=cart_id)
        .select_related("sell", "sell__wine")
        .annotate(purchase_price=F("sell__sell_price") * F("cart_det_qnty"))
        .values(
            "sell__wine__wine_image",
            "sell__wine__wine_name",
            "sell__sell_id",
            "sell__sell_price",
            "cart_det_qnty",
            "purchase_price",
            "cart_det_id",
        )
    )
    return info


def get_store_lists(wine_id: str) -> QuerySet:
    """
    SELECT `win_sell`.`sell_id`,
       `win_wine`.`wine_name`,
       `win_sell`.`sell_price`,
       `win_store`.`store_name`,
       `win_store`.`store_address`
    FROM `win_sell`
    INNER JOIN `win_wine`
    ON (`win_sell`.`wine_id` = `win_wine`.`wine_id`)
    INNER JOIN `win_store`
    ON (`win_sell`.`store_id` = `win_store`.`store_id`)
    WHERE `win_sell`.`wine_id` = wine_id
    """

    store_lists = (
        WinSell.objects.filter(wine_id=wine_id, sell_state=1)
        .select_related("wine", "store")
        .annotate(
            wine_name=F("wine__wine_name"),
            store_name=F("store__store_name"),
            store_address=F("store__store_address"),
        )
        .values(
            "sell_id",
            "wine_name",
            "sell_price",
            "store_name",
            "store_address",
        )
    )

    return store_lists


class StoreListSerializer(serializers.Serializer):
    sell_id = serializers.IntegerField()
    wine_name = serializers.CharField()
    sell_price = serializers.IntegerField()
    store_name = serializers.CharField()
    store_address = serializers.CharField()


def get_product_info(sell_id: str) -> dict:
    """
    SELECT `win_sell`.`sell_id`,
       `win_wine`.`wine_image`,
       `win_wine`.`wine_name`,
       `win_wine`.`wine_alc`,
       `win_store`.`store_name`,
       `win_store`.`store_address`,
       `win_store_url`.`store_map_url`,
       `win_sell`.`sell_promot`,
       `win_sell`.`sell_price`
    FROM `win_sell`
    INNER JOIN `win_wine`
    ON (`win_sell`.`wine_id` = `win_wine`.`wine_id`)
    INNER JOIN `win_store`
    ON (`win_sell`.`store_id` = `win_store`.`store_id`)
    LEFT OUTER JOIN `win_store_url`
    ON (`win_store`.`store_id` = `win_store_url`.`store_id`)
    WHERE `win_sell`.`sell_id` = sell_id
    """

    product_info = (
        WinSell.objects.select_related("store", "wine")
        .filter(sell_id=sell_id)
        .prefetch_related("store__storeUrl")
        .values(
            "sell_id",
            "wine__wine_image",
            "wine__wine_name",
            "wine__wine_alc",
            "store__store_name",
            "store__store_address",
            "store__storeUrl__store_map_url",
            "sell_promot",
            "sell_price",
        )
    )

    return product_info


def get_info_of_buy_one(sell_id: str) -> QuerySet:
    """
    SELECT `win_wine`.`wine_image`,
       `win_wine`.`wine_name`,
       `win_sell`.`sell_price`
    FROM `win_sell`
    INNER JOIN `win_wine`
    ON (`win_sell`.`wine_id` = `win_wine`.`wine_id`)
    WHERE `win_sell`.`sell_id` = sell_id
    """

    info = (
        WinSell.objects.select_related("wine")
        .filter(sell_id=sell_id)
        .values("wine__wine_image", "wine__wine_name", "sell_price")
    )[0]

    return info


def get_user_point(user_id: str) -> int:
    """
    SELECT `win_user`.`user_point`
    FROM `win_user`
    WHERE `win_user`.`user_id` = 'user_id'
    """

    user_point = int(
        WinUser.objects.filter(user_id=user_id)
        .values("user_point")[0]
        .get("user_point")
    )
    return user_point


def get_enc_receive_codes(cart_detail_id: str) -> list:
    pass


def get_detail_info(purchase_id):
    """
    SELECT *
    FROM win_purchase wp
    INNER JOIN win_purchase_detail wpd
    ON wp.purchase_id = wpd.purchase_id
    INNER JOIN win_receive_code wrc
    ON wpd.purchase_detail_id = wrc.purchase_detail_id_id
    WHERE wp.purchase_id = 61
    """

    detail_infos = (
        WinReceiveCode.objects.select_related("purchase_detail_id")
        .select_related(
            "purchase_detail_id__sell",
            "purchase_detail_id__sell__wine",
            "purchase_detail_id__sell__store",
        )
        .filter(purchase_detail_id__purchase_id=purchase_id)
        .values(
            "purchase_detail_id__sell__wine__wine_name",
            "purchase_detail_id__purchase_det_number",
            "purchase_detail_id__purchase_det_price",
            "purchase_detail_id__sell__store__store_name",
            "purchase_detail_id__sell__store__store_address",
            "purchase_detail_id__sell__store__store_email",
            "receive_code",
        )
        .order_by("purchase_detail_id__sell__store__store_email")
    )

    return detail_infos


def get_product_reviews(sell_id: int, select_code: int) -> QuerySet:
    if select_code == 1:
        order = "-review_reg_time"
    elif select_code == 2:
        order = "-review_score"
    elif select_code == 3:
        order = "review_score"

    review_list = (
        WinReview.objects.filter(sell_id=sell_id)
        .annotate(
            year=ExtractYear("review_reg_time"),
            month=ExtractMonth("review_reg_time"),
            day=ExtractDay("review_reg_time"),
            hour=ExtractHour("review_reg_time"),
            minute=ExtractMinute("review_reg_time"),
            review_time=Concat(
                "year",
                V("-"),
                "month",
                V("-"),
                "day",
                V(" "),
                "hour",
                V(":"),
                "minute",
                output_field=CharField(),
            ),
        )
        .values("user_id", "review_content", "review_time", "review_score")
        .order_by(order)
    )

    list_length = review_list.count()
    if list_length > 5:
        return review_list[:6]

    elif list_length <= 5 and list_length >= 1:
        return review_list


class ReviewSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    review_content = serializers.CharField()
    review_time = serializers.CharField()
    review_score = serializers.IntegerField()


def get_user_name_and_email(user_id):
    name_and_email = WinUser.objects.filter(user_id=user_id).values_list(
        "user_name", "user_email"
    )[0]
    return name_and_email
