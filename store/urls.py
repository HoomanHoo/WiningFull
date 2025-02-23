from django.urls.conf import path
from store import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(
        "registration",
        views.StoreRegistrationView.as_view(),
        name="storeRegistration",
    ),
    path(
        "regnums/<str:regnum>",
        views.CheckStoreRegistNumberView.as_view(),
        name="checkRegistNumber",
    ),
    path(
        "product/addition",
        views.ProductAdditionView.as_view(),
        name="productAddition",
    ),
    path(
        "product/addition/<str:mdfy>",
        views.ProductAdditionView.as_view(),
        name="productAdditionPageModify",
    ),
    path(
        "product/pages/<int:page_num>",
        views.ProductListView.as_view(),
        name="productPages",
    ),
    path("mypage", views.StoreMyPageView.as_view(), name="storeMyPage"),
    # path("search/product", views.SearchProduct.as_view(), name="searchProduct"),
    path("info", views.StoreInfoView.as_view(), name="storeInfo"),
    path(
        "search/receive-code",
        views.SearchReceiveCodeView.as_view(),
        name="searchReceiveCode",
    ),
    path(
        "info/modification",
        views.StoreInfoModificationView.as_view(),
        name="storeInfoModification",
    ),
    path(
        "sell/histories/pages/<int:page_num>",
        views.SellDetailListView.as_view(),
        name="sellDetailList",
    ),
    path(
        "sell/merchandises/pages/<int:page_num>",
        views.SellMerchandiseView.as_view(),
        name="sellList",
    ),
    path(
        "discontinue-product",
        views.DiscontinueProductView.as_view(),
        name="discontinueProduct",
    ),
    path("info/drop-store", views.DropStoreView.as_view(), name="dropStore"),
    path(
        "revenue/pages/<int:page_num>",
        views.StoreRevenueMainView.as_view(),
        name="storeRevenue",
    ),
    path(
        "revenue/pages/<int:page_num>/term/<int:term>",
        views.StoreRevenueTermView.as_view(),
    ),
    path("receive-code/codes/<str:code>", views.SearchReceiveCodeApi.as_view()),
    path(
        "sell/merchandises/<int:sell_id>/reviews",
        views.StoreReviewView.as_view(),
        name="merchandiseReview",
    ),
    path(
        "sell/merchandises/<int:sell_id>/reviews/<int:page_num>",
        views.StoreReviewListView.as_view(),
    ),
]


urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_URL
)  # MEDIA 경로 추가
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # MEDIA 경로 추가
