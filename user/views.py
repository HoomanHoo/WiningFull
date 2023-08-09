import base64
import json
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import requests
from Wining import settings
from purchasing.usecase import decrypt_receive_code
from store.usecase.pagination import db_preprocessing, pagenation
from user.db_access.query_set import (
    check_id,
    check_login,
    get_favorite_info,
    insert_user_info,
)
from user.kakao_token_module import kakao_token
from user.models import (
    WinUser,
    WinUserAccount,
    WinUserGrade,
    WinUserFavorite,
    WinReview,
    WinPointHis,
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateformat import DateFormat
from datetime import datetime
from board.models import WinBoard, WinComment, WinBoardImg
from store.models import WinSell
from purchasing.models import (
    WinPurchase,
    WinPurchaseDetail,
    WinCart,
    WinReceiveCode,
    WinCartDetail,
)
from detail.models import WinDetailView
from django.contrib.messages.context_processors import messages
from django.urls.base import reverse
from django.db.models import F
from django.core.files.storage import default_storage
from purchasing.usecase.decrypt_receive_code import DecModule
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from user.serializers.serializers import (
    AccountPatchSerializer,
    AccountSerializer,
    SelectAccountSerializer,
    WinUserAccountSerializer,
)

logger = logging.getLogger("user")


class LoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("user/login.html")
        refusal = int(request.GET.get("refusal", 3))
        if refusal == 1:
            context = {"refusal": 1}
        elif refusal == 2:
            context = {"refusal": 2}
        else:
            context = {"refusal": 3}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = request.POST["user_id"]
        user_passwd = request.POST["user_passwd"]
        result = check_login(user_id=user_id, is_kakao=False, user_passwd=user_passwd)

        if result == 1:
            request.session["memid"] = user_id
            return redirect("myPage")

        elif result == -1:
            message = "탈퇴한 회원입니다"

        elif result == -2:
            message = "입력하신 비밀번호가 다릅니다"

        elif result == -3:
            message = "입력하신 아이디가 없습니다"

        template = loader.get_template("user/login.html")
        context = {
            "message": message,
        }

        return HttpResponse(template.render(context, request))


class KakaoLogoutView(View):
    def get(self, request):
        REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
        LOGOUT_REDIRECT_URI = getattr(settings, "LOGOUT_REDIRECT_URI")

        logout_url = (
            "https://kauth.kakao.com/oauth/logout?client_id="
            + REST_API_KEY
            + "&logout_redirect_uri="
            + LOGOUT_REDIRECT_URI
        )

        return redirect(logout_url)


class LogoutView(View):
    def get(self, request):
        ACCESS_TOKEN = request.session.get("access_Token", None)

        if ACCESS_TOKEN is None:
            del request.session["memid"]

            return redirect("login")

        else:
            del request.session["access_Token"]
            del request.session["memid"]

            return redirect("login")


# return redirect("user/login.html")


class KaKaoLogin(View):
    def get(self, request, **kwargs):
        act = request.GET.get("act", None)

        if act is None:
            act = kwargs.get("act", None)
        REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")

        if act == "login":
            KAKAO_REDIRECT_URI = getattr(settings, "KAKAO_REDIRECT_URI1")

        elif act == "regist":
            KAKAO_REDIRECT_URI = getattr(settings, "KAKAO_REDIRECT_URI2")

        elif act == "regstore":
            KAKAO_REDIRECT_URI = getattr(settings, "KAKAO_REDIRECT_URI3")

        uri = (
            "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id="
            + REST_API_KEY
            + "&redirect_uri="
            + KAKAO_REDIRECT_URI
            + "&response_type=code&scope="
            + "account_email,age_range"
        )

        return redirect(uri)


class KakaoRedirectURI(View):
    def get(self, request):
        code = request.GET.get("code", None)
        KAKAO_REDIRECT_URI = getattr(settings, "KAKAO_REDIRECT_URI1")

        result = kakao_token(code=code, redirect_uri=KAKAO_REDIRECT_URI, is_store=0)

        if result["code"] == -1:
            return redirect("kakaoLoginRefresh", act="login")

        else:
            user_email = result["email"]
            min_age = result["min_age"]

            if int(min_age) < 20:  # 미성년자 일 때
                template = loader.get_template("user/return.html")
                context = {"code": -1}
                return HttpResponse(template.render(context, request))

            else:  # 회원 정보 있는지 검증
                check_result = check_login(user_id=user_email, is_kakao=True)

                if check_result == -3 or check_result == -1:  # 회원 정보가 없거나 탈퇴 회원일 때
                    template = loader.get_template("user/return.html")
                    context = {"code": -2}
                    return HttpResponse(template.render(context, request))

                else:  # 로그인 성공
                    request.session["memid"] = user_email
                    request.session["access_Token"] = result["access_token"]
                    return redirect("myPage")


class InputUserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        code = request.GET.get("code", None)
        KAKAO_REDIRECT_URI = getattr(settings, "KAKAO_REDIRECT_URI2")

        result = kakao_token(code=code, redirect_uri=KAKAO_REDIRECT_URI, is_store=0)
        if result["code"] == -1:
            return redirect("kakaoLoginRefresh", act="regist")
        else:
            user_email = result["email"]
            min_age = result["min_age"]
            if int(min_age) < 20:
                template = loader.get_template("user/return.html")
                context = {"code": -1}
                return HttpResponse(template.render(context, request))

            else:
                template = loader.get_template("user/inputUser.html")
                context = {
                    "user_email": user_email,
                }
            return HttpResponse(template.render(context, request))

    def post(self, request):
        user_point = 0
        # default_grade = 1
        try:
            dto = WinUser(
                user_id=request.POST["user_id"],
                user_grade=WinUserGrade.objects.get(user_grade=1),
                user_passwd=request.POST["user_passwd"],
                user_name=request.POST["user_name"],
                user_email=request.POST["user_email"],
                user_tel=request.POST["user_tel"],
                user_reg_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_point=user_point,
            )

            fdto = WinUserFavorite(
                user=WinUser.objects.get(user_id=dto.user_id),
                fav_wine_color=request.POST["color"],
                fav_alc=request.POST["alc"],
                fav_numbwith=request.POST["comp_num"],
                fav_sweet=request.POST["sweet"],
                fav_bitter=request.POST["bitter"],
                fav_sour=request.POST["sour"],
                fav_season=request.POST["season"],
                fav_food=request.POST["food"],
                fav_first_priority=request.POST["fav_first"],
                fav_second_priority=request.POST["fav_second"],
                fav_third_priority=request.POST["fav_third"],
            )

            try:
                insert_user_info(user_info=dto, user_favorite_info=fdto)

            except Exception as ex:
                logger.error(ex)
                return redirect("inputUserInfo")

            # message = "회원가입에 성공했습니다"
            # alert_script = f'<script>alert("{message}");</script>'

            return redirect("login")

        except Exception:
            return redirect("inputUserInfo")


class InputStoreView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        code = request.GET.get("code", None)
        KAKAO_REDIRECT_URI = getattr(settings, "KAKAO_REDIRECT_URI3")

        result = kakao_token(code=code, redirect_uri=KAKAO_REDIRECT_URI, is_store=1)
        if result["code"] == -1:
            return redirect("kakaoLoginRefresh", act="regstore")
        else:
            user_email = result["email"]
            min_age = result["min_age"]
            if int(min_age) < 20:
                template = loader.get_template("user/return.html")
                context = {"code": -1}
                return HttpResponse(template.render(context, request))

            else:
                template = loader.get_template("user/inputStore.html")
                context = {
                    "user_email": user_email,
                }
                request.session["access_Token"] = result["access_token"]
            return HttpResponse(template.render(context, request))

    def post(self, request):
        user_point = 0
        try:
            user_id = request.POST["user_id"]
            # user_input =
            dto = WinUser(
                user_id=user_id,
                user_grade=WinUserGrade.objects.get(user_grade=1),
                user_passwd=request.POST["user_passwd"],
                user_name=request.POST["user_name"],
                user_email=request.POST["user_email"],
                user_tel=request.POST["user_tel"],
                user_reg_date=DateFormat(datetime.now()).format("Y-m-d h:i:s"),
                user_point=user_point,
            )
            insert_user_info(user_info=dto, is_store=True)
            request.session["temp_id"] = user_id

            # return redirect("/store/store-registration")
            return redirect("storeRegistration")
        except Exception:
            return redirect("inputStore")

        # 로그인도 회원가입도 되지 않았을 때 가입 시 입력 아이디를 세션에 저장한다.
        # redirect로 이동한다. context에 id를 넣어 보내면 주소가 이동하지 않고 redirect 를 쓰면 id를 보낼 수 없다.
        # 그래서 로그인하지 않았지만 회원가입 시 임시로 입력한 id를 세션에 저장하고 store 에서 꺼내 쓴다.


class ConfirmIdView(View):
    def get(self, request):
        template = loader.get_template("user/confirmId.html")
        user_id = request.GET["user_id"]
        result = 0

        result = check_id(user_id=user_id)
        context = {"result": result["result"], "user_id": user_id}

        return HttpResponse(template.render(context, request))


class DeleteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("user/delete.html")
        user_id = request.session.get("memid")
        context = {"user_id": user_id}

        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = request.POST["user_id"]
        user_passwd = request.POST["user_passwd"]

        dto = check_id(user_id=user_id)["user_info"]

        if user_passwd == dto.user_passwd:
            w_user_grade = WinUserGrade.objects.get(user_grade=-1)
            dto.user_grade.user_grade = -1
            dto.save()

            ACCESS_TOKEN = request.session.get(
                "access_Token", None
            )  # access token = none이면 login으로 리다이렉트 하거나 refresh 토큰으로 업데이트해야함

            if ACCESS_TOKEN is None:
                del request.session["memid"]

                return redirect("login")
            else:
                request_header = {
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                }

                logout_url = "https://kapi.kakao.com/v1/user/unlink"

                requests.post(logout_url, headers=request_header)
                del request.session["access_Token"]
                del request.session["memid"]

                return redirect("login")
        else:
            template = loader.get_template("user/delete.html")
            message = "입력하신 비밀번호가 다릅니다"
            context = {"user_id": user_id, "message": message}

            return HttpResponse(template.render(context, request))


class ModifyUserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("user/modifyUser.html")
        user_id = request.session.get("memid")
        dto = check_id(user_id=user_id)["user_info"]

        if dto.user_grade_id == 1:
            fdto = get_favorite_info(user_id=user_id)

            if fdto is None:
                context = {"user_id": user_id, "dto": dto}

            else:
                context = {"user_id": user_id, "dto": dto, "fdto": fdto}

        return HttpResponse(template.render(context, request))

    # 여기까지 코드 정리 진행됨 - 집 가서 다시 보기
    def post(self, request):
        user_id = request.session.get("memid")
        dto = WinUser.objects.get(user_id=user_id)

        dto.user_passwd = request.POST["user_passwd"]
        dto.user_email = request.POST["user_email"]
        dto.user_tel = request.POST["user_tel"]

        dto.save()

        try:
            fdto = WinUserFavorite.objects.get(user_id=user_id)

            fdto.fav_wine_color = request.POST["color"]
            fdto.fav_alc = request.POST["alc"]
            fdto.fav_numbwith = request.POST["comp_num"]
            fdto.fav_sweet = request.POST["sweet"]
            fdto.fav_bitter = request.POST["bitter"]
            fdto.fav_sour = request.POST["sour"]
            fdto.fav_season = request.POST["season"]
            fdto.fav_food = request.POST["food"]
            fdto.fav_first_priority = request.POST["fav_first"]
            fdto.fav_second_priority = request.POST["fav_second"]
            fdto.fav_third_priority = request.POST["fav_third"]

            fdto.save()

        except WinUserFavorite.DoesNotExist:
            fdto = WinUserFavorite.objects.create(user_id=user_id)

            fdto.fav_wine_color = request.POST["color"]
            fdto.fav_alc = request.POST["alc"]
            fdto.fav_numbwith = request.POST["comp_num"]
            fdto.fav_sweet = request.POST["sweet"]
            fdto.fav_bitter = request.POST["bitter"]
            fdto.fav_sour = request.POST["sour"]
            fdto.fav_season = request.POST["season"]
            fdto.fav_food = request.POST["food"]
            fdto.fav_first_priority = request.POST["fav_first"]
            fdto.fav_second_priority = request.POST["fav_second"]
            fdto.fav_third_priority = request.POST["fav_third"]

            fdto.save()

        return redirect("myPage")


class MyPageView(View):
    def get(self, request):
        template = loader.get_template("user/myPage.html")
        memid = request.session.get("memid")
        dto = WinUser.objects.get(user_id=memid)
        purchase_c = WinPurchase.objects.filter(user_id=memid).count()
        review_c = WinReview.objects.filter(user_id=memid).count()
        cart_c = (
            WinCartDetail.objects.select_related("cart")
            .filter(cart__user_id=memid)
            .count()
        )
        detail_v = (
            WinDetailView.objects.filter(user_id=memid)
            .order_by("-detail_view_time")[:6]
            .select_related("wine")
        )
        user_grade = dto.user_grade_id

        wine_images = []

        for v in detail_v:
            wine_images.append([v.wine.wine_image, v.wine.wine_id])

        print(detail_v)
        print(wine_images)

        if memid:
            context = {
                "memid": memid,
                "dto": dto,
                "purchase_c": purchase_c,
                "review_c": review_c,
                "cart_c": cart_c,
                "wine_images": wine_images,
                "user_grade": user_grade,
            }
        else:
            context = {}

        return HttpResponse(template.render(context, request))


class ReviewListView(View):
    def get(self, request):
        template = loader.get_template("user/reviewList.html")
        user_id = request.session.get("memid")
        dtos = WinReview.objects.filter(user_id=user_id).order_by("-review_reg_time")

        context = {"dtos": dtos}

        return HttpResponse(template.render(context, request))


class ReviewWriteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("user/reviewWrite.html")
        sell_id = request.GET.get("sell_id")
        dto = WinSell.objects.get(sell_id=sell_id)
        context = {"dto": dto}

        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = request.session.get("memid")
        sell_id = request.POST.get("sell_id")
        dto = WinReview(
            user=WinUser.objects.get(user_id=user_id),
            sell_id=sell_id,
            review_content=request.POST["content"],
            review_score=request.POST["rating"],
            review_reg_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        dto.save()

        return redirect("reviewList")


class PurchaseDetailView(View):
    def get(self, request):
        template = loader.get_template("user/purchaseDetail.html")
        user_id = request.session.get("memid")
        # dtos = WinPurchase.objects.filter(user_id = user_id)
        purchases = WinPurchase.objects.filter(user_id=user_id).order_by(
            "-purchase_time"
        )
        reviews = WinReview.objects.filter(user_id=user_id).values_list(
            "sell_id", flat=True
        )
        dtos = []

        for purchase in purchases:
            purchase_details = WinPurchaseDetail.objects.filter(purchase_id=purchase)

            for purchase_detail in purchase_details:
                wine_name = purchase_detail.sell.wine.wine_name
                wine_name_eng = purchase_detail.sell.wine.wine_name_eng
                wine_image = purchase_detail.sell.wine.wine_image
                purchase_price = purchase_detail.purchase_det_price
                purchase_number = purchase_detail.purchase_det_number
                purchase_time = purchase_detail.purchase.purchase_time
                sell_id = purchase_detail.sell.sell_id
                purchase_det_state = purchase_detail.purchase_det_state

                print(purchase_det_state)

                dtos.append(
                    {
                        "wine_name": wine_name,
                        "wine_name_eng": wine_name_eng,
                        "wine_image": wine_image,
                        "purchase_price": purchase_price,
                        "purchase_number": purchase_number,
                        "purchase_time": purchase_time,
                        "sell_id": sell_id,
                        "purchase_det_state": purchase_det_state,
                    }
                )

        context = {"dtos": dtos, "reviews": reviews}

        return HttpResponse(template.render(context, request))


class MyBoardView(View):
    def get(self, request):
        template = loader.get_template("user/myBoard.html")
        user_id = request.session.get("memid")
        dtos = WinBoard.objects.filter(user_id=user_id).order_by("-board_reg_time")

        print(dtos)
        print(dtos.count())

        board_images = []

        for dto in dtos:
            images = WinBoardImg.objects.filter(board=dto)

            if images.exists():
                board_images.append(images[0].board_image)

            else:
                board_images.append("")

        dtos_and_images = zip(dtos, board_images)

        for dto in dtos:
            print(dto.board_reg_time)
            print(dto.board_read_count)
            print(dto.board_title)
            print(dto.board_content)
            print(board_images)

        context = {
            "dtos_and_images": dtos_and_images,
            "user_id": user_id,
        }

        return HttpResponse(template.render(context, request))


class MyCommentView(View):
    def get(self, request):
        template = loader.get_template("user/myComment.html")
        user_id = request.session.get("memid")
        dtos = (
            WinComment.objects.select_related("board")
            .filter(user_id=user_id)
            .order_by("-comment_reg_time")
        )

        for dto in dtos:
            print(dto.board.board_title)

        context = {"dtos": dtos}

        return HttpResponse(template.render(context, request))


class AddPointView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("user/addPoint.html")
        memid = request.session.get("memid")
        dto = WinUser.objects.get(user_id=memid)

        context = {"dto": dto}

        return HttpResponse(template.render(context, request))

    def post(self, request):
        chargepoint = int(request.POST["point"])
        user_id = request.session.get("memid")
        dto = WinUser.objects.get(user_id=user_id)
        user_point = dto.user_point + chargepoint

        dto.user_point = user_point
        dto.save()

        pdto = WinPointHis(
            user=WinUser.objects.get(user_id=dto.user_id),
            point_reg=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            point_add=chargepoint,
        )

        pdto.save()

        return redirect("myPage")


class SearchUserAccountAPI(APIView):
    def get(self, request):
        user_id = request.session.get("memid")
        # user_id = "test9090"

        try:
            user_account_info = WinUserAccount.objects.get(user_id=user_id)
            account_default_setting = user_account_info.user_account_default

            if account_default_setting == 1:
                user_account = {"user_account": user_account_info.user_account1}
                user_account["user_account_id"] = user_account_info.user_account_id

            elif account_default_setting == 2:
                user_account = {"user_account": user_account_info.user_account2}
                user_account["user_account_id"] = user_account_info.user_account_id

            elif account_default_setting == 3:
                user_account = {"user_account": user_account_info.user_account3}
                user_account["user_account_id"] = user_account_info.user_account_id

        except ObjectDoesNotExist as ex:
            logger.info(ex)
            user_account = {"user_account": "결제 수단이 등록되지 않았습니다"}
            user_account["user_account_id"] = -1

        serialized = SelectAccountSerializer(user_account)
        json_result = JSONRenderer().render(serialized.data)

        return Response(json_result)


class UpdateUserDefaultAccountAPI(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        account_id = kwargs.get("account_id", None)
        # user_id = "test9090"
        user_account_info = WinUserAccount.objects.filter(
            user_account_id=account_id
        ).values("user_account1", "user_account2", "user_account3")[0]

        serialized = AccountSerializer(user_account_info)
        json_result = JSONRenderer().render(serialized.data)

        return Response(json_result)

    def patch(self, request, *args, **kwargs):
        select_account = request.data.get("selectedAccount")
        account_id = kwargs.get("account_id", None)
        data = {"user_account_id": account_id, "user_account_default": select_account}

        try:
            instance = WinUserAccount.objects.get(pk=account_id)

            serializer = AccountPatchSerializer(
                instance=instance, data=data, partial=True
            )
            if serializer.is_valid():
                update_data = serializer.save()
                account_default_setting = update_data.user_account_default
                if account_default_setting == 1:
                    user_account = {"user_account": update_data.user_account1}

                elif account_default_setting == 2:
                    user_account = {"user_account": update_data.user_account2}

                elif account_default_setting == 3:
                    user_account = {"user_account": update_data.user_account3}

                user_account["user_account_id"] = update_data.user_account_id

                serialized = SelectAccountSerializer(user_account)
                json_result = JSONRenderer().render(serialized.data)

                return Response(json_result)

        except ObjectDoesNotExist as ex:
            logger.info(ex)
            user_account = {"user_account": "결제 수단이 등록되지 않았습니다"}
            updated_serialize = WinUserAccountSerializer(instance)
            json_result = JSONRenderer().render(updated_serialize.data)
            return Response(json_result, status=500)


class InsertPaymentMethodView(View):
    def get(self, request):
        template = loader.get_template("user/paymentMethod.html")
        context = {}
        return HttpResponse(template.render(context, request))


class InsertPaymentMethodAPI(APIView):
    pass


class AddPointHisView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("user/addPointHis.html")
        memid = request.session.get("memid")
        dtos = WinPointHis.objects.filter(user_id=memid).order_by("-point_reg")

        context = {
            "dtos": dtos,
        }

        return HttpResponse(template.render(context, request))


class MyReceiveCodeView(View):
    def get(self, request):
        template = loader.get_template("user/myReceiveCode.html")
        page_num = request.GET.get("pageNum", 1)
        show_length = 30
        end = int(show_length) * int(page_num)
        start = end - int(show_length)
        user_id = request.session.get("memid")
        dtos = (
            WinReceiveCode.objects.annotate(
                purchase_det_number=F("purchase_detail__purchase_det_number"),
                purchase_det_price=F("purchase_detail__purchase_det_price"),
                store_name=F("purchase_detail__sell__store__store_name"),
                user_name=F("purchase_detail__purchase__user__user_name"),
                user_id=F("purchase_detail__purchase__user__user_id"),
                wine_name=F("purchase_detail__sell__wine__wine_name"),
                purchase_state=F("purchase_detail__purchase_det_state"),
            )
            .filter(user_id=user_id)
            .values(
                "purchase_detail_id",
                "purchase_det_number",
                "purchase_det_price",
                "purchase_state",
                "store_name",
                "wine_name",
                "receive_code",
            )
        )

        db_data = db_preprocessing(db_data=dtos, end_page=end, start_page=start)

        result = pagenation(
            show_length=show_length,
            page_num=page_num,
            end_page=end,
            start_page=start,
            datas=db_data,
        )
        pages_count = result["pages_count"]
        db_data = result["db_data"]
        state = result["state"]
        list_dtos = list(db_data)

        for list_dto in list_dtos:
            list_dto["receive_code"] = base64.b64decode(
                list_dto["receive_code"]
            ).decode("utf-8")

        context = {"pdtos": list_dtos, "pages_count": pages_count, "state": state}
        return HttpResponse(template.render(context, request))


class TempLoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("purchasing/tempLogin.html")
        logger.info("temp login")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        req_data = json.loads(request.body)

        user_id = req_data.get("id", None)
        user_passwd = req_data.get("passwd", None)

        try:
            dto = WinUser.objects.get(user_id=user_id)
            user_grade = dto.user_grade.user_grade

            if user_passwd == dto.user_passwd:
                if user_grade != -1:
                    request.session["memid"] = user_id
                    message = 1

                else:
                    message = -1

            else:
                message = -2
        except ObjectDoesNotExist as ex:
            logger.error(ex)
            message = -2

        logger.info(f"{user_id} temp login")
        context = {"message": message}

        return JsonResponse(context, status=200)
