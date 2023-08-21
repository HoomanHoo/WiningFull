from django.urls.conf import path
from user import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [  # init_url == "http://localhost:8000/user/login"
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.KakaoLogoutView.as_view(), name="logout"),
    path("locallogout", views.LogoutView.as_view(), name="localLogout"),
    path("inputUserInfo", views.InputUserView.as_view(), name="inputUserInfo"),
    path("inputStore", views.InputStoreView.as_view(), name="inputStore"),
    path("confirmId", views.ConfirmIdView.as_view(), name="confirmId"),
    path("delete", views.DeleteView.as_view(), name="delete"),
    path("myPage", views.MyPageView.as_view(), name="myPage"),
    path("modifyUser", views.ModifyUserView.as_view(), name="modifyUser"),
    path("reviewWrite", views.ReviewWriteView.as_view(), name="reviewWrite"),
    path("reviewList", views.ReviewListView.as_view(), name="reviewList"),
    path("purchaseDetail", views.PurchaseDetailView.as_view(), name="purchaseDetail"),
    path("myBoard", views.MyBoardView.as_view(), name="myBoard"),
    path("addPoint", views.AddPointView.as_view(), name="addPoint"),
    path("addPointHis", views.AddPointHisView.as_view(), name="addPointHis"),
    path("myComment", views.MyCommentView.as_view(), name="myComment"),
    path("myReceiveCode", views.MyReceiveCodeView.as_view(), name="myReceiveCode"),
    path("kakaologin", views.KaKaoLogin.as_view(), name="kakaoLogin"),
    path("kakaologin/<str:act>", views.KaKaoLogin.as_view(), name="kakaoLoginRefresh"),
    path("inputUser", views.KakaoRedirectURI.as_view(), name="inputUser"),
    path("templogin", views.TempLoginView.as_view(), name="tempLogin"),
    path(
        "account",
        views.SearchUserAccountAPI.as_view(),
        name="searchUserAccount",
    ),
    path(
        "account/<int:account_id>",
        views.UpdateUserDefaultAccountAPI.as_view(),
        name="updateDefaultAccount",
    ),
    path(
        "payment-method", views.InsertPaymentMethodView.as_view(), name="paymentMethod"
    ),
    path(
        "payment-method-api",
        views.InsertPaymentMethodAPI.as_view(),
        name="paymentMethodAPI",
    ),
]

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_URL
)  # MEDIA 경로 추가
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # MEDIA 경로 추가

