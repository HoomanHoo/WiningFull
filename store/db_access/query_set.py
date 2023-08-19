import time
from django.db import transaction
from django.db.models import F
from django.db.models.query import QuerySet
from django.db.models.aggregates import Sum
from django.db.models.fields import CharField
from django.db.models.functions.datetime import (
    TruncDate,
    TruncMonth,
    TruncQuarter,
    TruncYear,
)
from django.db.models.functions.comparison import Cast
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from detail.models import WinWine
from purchasing.models import WinPurchase, WinPurchaseDetail, WinReceiveCode
from store.models import WinStore, WinStoreUrl, WinSell
from user.models import WinReview, WinUser, WinUserGrade


@transaction.atomic
def insert_store_info(
    user_id: str,
    store_address: str,
    store_name: str,
    store_reg_num: str,
    store_email: str,
    store_map_url: str,
) -> None:
    try:
        store = WinStore.objects.get(user_id=user_id)

        # store = store[0]

        store.store_id = store.store_id
        store.store_address = store_address
        store.store_name = store_name
        store.store_reg_num = store_reg_num
        store.store_email = store_email

    except ObjectDoesNotExist as ex:
        print(ex)
        store = WinStore(
            user_id=user_id,
            store_address=store_address,
            store_name=store_name,
            store_reg_num=store_reg_num,
            store_email=store_email,
        )

    store.save()

    try:
        store_url = WinStoreUrl.objects.get(store_id=store.store_id)
        print("try")
        if store_map_url == "":
            print("No URL!")
            store_url.delete()
        else:
            print("try-else")
            store_url.store_map_url = store_map_url
            store_url.save()
    except ObjectDoesNotExist as ex:
        print(ex)
        store_url = WinStoreUrl(store_id=store.store_id, store_map_url=store_map_url)
        store_url.save()


@transaction.atomic
def insert_sell_info(
    user_id: str,
    store_id: str,
    wine_ids: list,
    current_time: str,
    sell_ids: list,
    sell_prices: list,
    sell_promots: list,
    sell_state: int,
) -> None:
    win_sells_add = []
    win_sells_update = []
    for idx, wine_id in enumerate(wine_ids):
        if idx < len(sell_ids):
            win_sell = WinSell(
                sell_id=sell_ids[idx],
                wine_id=wine_id,
                sell_reg_time=current_time,
                sell_price=sell_prices[idx],
                sell_promot=sell_promots[idx],
                sell_state=sell_state,
            )
            win_sells_update.append(win_sell)
        else:
            win_sell = WinSell(
                store_id=store_id,
                wine_id=wine_ids[idx],
                sell_reg_time=current_time,
                sell_price=sell_prices[idx],
                sell_promot=sell_promots[idx],
                sell_state=sell_state,
            )
            win_sells_add.append(win_sell)

    WinSell.objects.bulk_update(
        win_sells_update,
        ["wine_id", "sell_reg_time", "sell_price", "sell_promot", "sell_state"],
    )
    WinSell.objects.bulk_create(win_sells_add)
    win_user = WinUser.objects.get(user_id=user_id)
    win_user.user_grade = WinUserGrade.objects.get(user_grade=2)
    win_user.save()


def delete_product(wine_id: str, user_id: str):
    WinSell.objects.filter(wine_id=wine_id, store__user_id=user_id).update(
        sell_state=-1
    )


def delete_user_info(user_id):
    user_info = WinUser.objects.filter(user_id=user_id)
    print(user_info)
    result = user_info.delete()
    print(result)


@transaction.atomic
def delete_store_info(store_id: str) -> None:
    store_url = WinStoreUrl.objects.filter(store_id=store_id)
    if len(store_url) == 1:
        store_url.delete()

    store_info = WinStore.objects.filter(store_id=store_id)
    store_info.delete()


@transaction.atomic  # 조인해서 업데이트 하는 법 있는지 확인할 것
def drop_store_info(user_id: str) -> None:
    WinUser.objects.filter(user_id=user_id).update(user_grade=1)
    WinStore.objects.filter(user_id=user_id).update(store_state=-1)
    WinSell.objects.filter(store__user_id=user_id).update(sell_state=-1)


def update_purchase_det_state(purchase_detail_id: str) -> None:
    WinPurchaseDetail.objects.filter(
        purchase_detail_id=purchase_detail_id,
    ).update(purchase_det_state=2)


def check_store_product_info(user_id: str) -> dict or None:
    info = (
        WinSell.objects.select_related("store")
        .filter(store__user_id=user_id)
        .values("sell_id")
        .first()
    )

    return info


def check_passwd(user_id: str, passwd: str) -> int:
    result = WinUser.objects.filter(user_id=user_id, user_passwd=passwd).count()
    return result


def check_store_regist_number(reg_num: str) -> bool:
    result = (
        WinStore.objects.filter(store_reg_num=reg_num).values("store_reg_num").count()
    )

    if result == 0:
        return True
    else:
        return False


def get_store_info(user_id: str) -> QuerySet:
    store_info = (
        WinStore.objects.filter(user_id=user_id)
        .prefetch_related("storeUrl")
        .values(
            "store_id",
            "user_id",
            "store_address",
            "store_name",
            "store_reg_num",
            "store_email",
            "storeUrl__store_map_url",
        )
    )[0]
    print(type(store_info))
    return store_info


def get_detail_sell_list(user_id: str):
    # store_id = WinStore.objects.get(user_id=user_id)

    detail_sell_list = (
        WinSell.objects.select_related("sellPurchaseDetail", "wine")
        .filter(store__user_id=user_id)
        .values(
            "sellPurchaseDetail__purchase_detail_id",
            "wine__wine_name",
            "sellPurchaseDetail__purchase_det_number",
            "sellPurchaseDetail__purchase_det_price",
            "sellPurchaseDetail__purchase_det_state",
        )
        .order_by("-sellPurchaseDetail__purchase_detail_id")
        .exclude(sellPurchaseDetail__purchase_detail_id=None)
    )

    return detail_sell_list


def get_product_list() -> QuerySet:
    wines = WinWine.objects.values("wine_id", "wine_name", "wine_capacity", "wine_alc")

    return wines


def search_product_list(search_keyword):
    result = WinWine.objects.filter(
        wine_name__icontains=search_keyword, wine_name__range=("가", "힣")
    ).values("wine_id", "wine_name", "wine_capacity", "wine_alc")

    return result


class PageSerializer(serializers.Serializer):
    def to_representation(self, instance):
        pages = instance["pages"]
        wines = self.context["wines"]

        return {"pages": pages, "wines": wines}


class ProductListSerializer(serializers.Serializer):
    wine_id = serializers.IntegerField()
    wine_name = serializers.CharField()
    wine_capacity = serializers.IntegerField()
    wine_alc = serializers.IntegerField()


def get_product_list_by_seller(user_id: str) -> QuerySet:
    product_list = (
        WinStore.objects.filter(user_id=user_id, storeSell__sell_state=1)
        .select_related("storeSell")
        .values(
            "storeSell__sell_id",
            "storeSell__wine__wine_id",
            "storeSell__wine__wine_name",
            "storeSell__sell_price",
            "storeSell__wine__wine_alc",
            "storeSell__wine__wine_capacity",
            "storeSell__sell_promot",
        )
    )

    return product_list


def get_store_revenue(user_id: str, term: int = 0):
    """ """

    sell_filter = WinSell.objects.filter(store__user_id=user_id).all()

    if term == 0:
        truncDate = Cast(TruncDate("purchase_time"), CharField())

    elif term == 1:
        truncDate = Cast(TruncMonth("purchase_time"), CharField())

    elif term == 2:
        truncDate = Cast(TruncQuarter("purchase_time"), CharField())

    elif term == 3:
        truncDate = Cast(TruncYear("purchase_time"), CharField())

    queryset = (
        WinPurchase.objects.annotate(date=truncDate)
        .select_related("purchasePurchaseDetail")
        .values("date")
        .filter(purchasePurchaseDetail__sell_id__in=sell_filter)
        .annotate(
            value_sum=Sum("purchasePurchaseDetail__purchase_det_price"),
            qnty_sum=Sum("purchasePurchaseDetail__purchase_det_number"),
        )
        .values("date", "value_sum", "qnty_sum")
        .order_by("-date")
    )

    return queryset


def search_receive_code(receive_code: str) -> str or dict:
    start = time.time()

    result = (
        WinReceiveCode.objects.annotate(
            purchase_det_number=F("purchase_detail__purchase_det_number"),
            purchase_det_price=F("purchase_detail__purchase_det_price"),
            store_name=F("purchase_detail__sell__store__store_name"),
            user_name=F("purchase_detail__purchase__user__user_name"),
            wine_name=F("purchase_detail__sell__wine__wine_name"),
            purchase_state=F("purchase_detail__purchase_det_state"),
            user_id=F("purchase_detail__purchase__user__user_id"),
        )
        .filter(receive_code=receive_code, purchase_state=1)
        .values(
            "purchase_detail_id",
            "purchase_det_number",
            "purchase_det_price",
            "store_name",
            "user_name",
            "wine_name",
            "user_id",
        )
    )
    end = time.time()
    print(end - start)
    print(len(result))
    if result.count() == 0:
        return {
            "purchase_detail_id": -1,
            "purchase_det_number": -1,
            "purchase_det_price": -1,
            "store_name": "",
            "user_name": "",
            "wine_name": "",
            "user_id": "",
        }

    else:
        return result[0]


class PurchaseDetailSerializer(serializers.ModelSerializer):
    store_name = serializers.ReadOnlyField()  # (source="store_name")
    user_name = serializers.ReadOnlyField()  # (source="user_name")
    user_id = serializers.ReadOnlyField()
    wine_name = serializers.ReadOnlyField()

    class Meta:
        model = WinPurchaseDetail
        fields = [
            "purchase_detail_id",
            "purchase_det_number",
            "purchase_det_price",
            "store_name",
            "user_name",
            "user_id",
            "wine_name",
        ]


def get_reviews_by_seller(sell_id: str):
    reviews = (
        WinReview.objects.annotate(reg_date=TruncDate("review_reg_time"))
        .filter(sell_id=sell_id)
        .values("user", "review_content", "review_score", "reg_date")
    )
    return reviews
