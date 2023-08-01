from django.urls.conf import path
from purchasing import views

app_name = "purchasing"
urlpatterns = [
    path(
        "wine/<int:wine_id>/stores",
        views.StoreListView.as_view(),
        name="storeList",
    ),
    path(
        "wine/<int:wine_id>/stores/<int:page_num>",
        views.LoadAdditionalStoreListAPI.as_view(),
        name="storeList",
    ),
    path(
        "sell/<int:sell_id>",
        views.DetailProductInfoView.as_view(),
        name="detailProductInfo",
    ),
    path(
        "sell/<int:sell_id>/reviews",
        views.ReviewLoadAPI.as_view(),
        name="reviewLoad",
    ),
    path("buy-list", views.BuyListView.as_view(), name="buyList"),
    path("add-cart-list", views.AddPickListView.as_view(), name="addCartList"),
    path("cart-list", views.PickListView.as_view(), name="cartList"),
    path("order-page", views.OrderPageView.as_view(), name="orderPage"),
    path("remove-buy-list", views.RemoveBuyList.as_view(), name="removeBuyList"),
]
