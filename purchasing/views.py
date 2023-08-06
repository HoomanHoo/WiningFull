import logging
import json
import base64

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat
from django.utils.datetime_safe import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from purchasing.usecase.receive_code_create_enc_module import (
    EncModule,
    create_receive_code,
)

from purchasing.usecase.purchase_usecase import calc, formating
from purchasing.db_access.query_set import (
    ReviewSerializer,
    StoreListSerializer,
    get_cart_state,
    get_product_info,
    get_info_of_buy_one,
    get_product_reviews,
    get_user_point,
    insert_enc_receive_codes,
    insert_purchase,
    get_store_lists,
    add_cart_info,
    get_cart_id,
    get_cart_list_page_info,
    get_detail_info,
)


from store.usecase.pagination import db_preprocessing
from purchasing.models import WinCartDetail, WinReceiveCode
from user.models import WinUser


logger = logging.getLogger("purchasing")


# Create your views here.
class StoreListView(View):
    def get(self, request, **kwargs):
        wine_id = kwargs.get("wine_id", None)
        page_num = 1
        template = loader.get_template("purchasing/storeList.html")
        show_length = 30
        end = int(show_length) * int(page_num)
        start = end - show_length
        store_list = get_store_lists(wine_id=wine_id)

        list_info = db_preprocessing(db_data=store_list, end_page=end, start_page=start)

        context = {"store_list": list_info[1]}
        logger.info(f"{request.session['memid']}: wine_id : {wine_id} StoreListView")
        return HttpResponse(template.render(context, request))


class LoadAdditionalStoreListAPI(APIView):
    def get(self, request, **kwargs):
        wine_id = kwargs.get("wine_id", None)
        page_num = kwargs.get("page_num", 1)

        show_length = 30
        end = int(show_length) * int(page_num)
        start = end - int(show_length)
        store_list = get_store_lists(wine_id=wine_id)

        list_info = db_preprocessing(db_data=store_list, end_page=end, start_page=start)

        db_data = list_info[1]
        serializer = StoreListSerializer(db_data, many=True)

        json_result = JSONRenderer().render(serializer.data)
        logger.info(
            f"{request.session['memid']}: wine_id : {wine_id} page_num: {page_num} LoadAdditionalStoreListAPI"
        )
        return Response(json_result)


class DetailProductInfoView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request, **kwargs):
        sell_id = kwargs.get("sell_id", 0)
        user_id = request.session.get("memid")

        template = loader.get_template("purchasing/detailProductInfo.html")

        product_info = get_product_info(sell_id=sell_id)
        print(product_info)

        if product_info:
            if product_info[0]["store__storeUrl__store_map_url"] == "":
                url_value = 0
                print(url_value)
            else:
                url_value = 1
                print(url_value)
            product_info = product_info[0]
        else:
            url_value = None  # 에러 페이지로 리다이렉트 시킬 것

        context = {
            "product_info": product_info,
            "url_value": url_value,
            "user_id": user_id,
            # "rdtos": rdtos,
        }
        logger.info(f"{user_id}: sell_id: {sell_id} DetailProductInfoView")
        return HttpResponse(template.render(context, request))


class ReviewLoadAPI(APIView):
    def get(self, request, **kwargs):
        sell_id = kwargs.get("sell_id", 0)
        select_code = int(request.GET.get("selectcode", 1))

        rdtos = get_product_reviews(sell_id=sell_id, select_code=select_code)

        serialzered = ReviewSerializer(rdtos, many=True)
        json_result = JSONRenderer().render(serialzered.data)

        logger.info(
            f"{request.session['memid']} : sell_id: {sell_id} select_code: {select_code} ReviewLoadAPI"
        )
        return Response(json_result)


class BuyListView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = request.session.get("memid")
        sell_id = request.GET.get("sellid", None)
        cart_id = request.GET.get("cartid", None)
        quantity = request.GET.get("qnty", None)
        user_point = get_user_point(user_id)
        template = loader.get_template("purchasing/buyList.html")
        context = {"user_point": user_point}
        dtos = []
        all_price = 0

        if user_id is None:
            logger.error("no user_id")
            redirect("purchaseError")

        if sell_id is not None:
            info = get_info_of_buy_one(sell_id)
            sell_price = info["sell_price"]

            dto = formating(
                user=user_id,
                product_info=sell_id,
                quantity=quantity,
                price_per_one=sell_price,
                wine_image=info["wine__wine_image"],
                wine_name=info["wine__wine_name"],
            )
            all_price = dto["purchase_price"]
            dtos.append(dto)

        elif cart_id is not None:
            cart_id = get_cart_id(user_id=user_id)

            infos = get_cart_list_page_info(cart_id=cart_id)

            for info in infos:
                all_price += info.get("purchase_price")
                dto = formating(
                    user=user_id,
                    identifier=info.get("cart_det_id"),
                    product_info=info.get("sell__sell_id"),
                    quantity=info.get("cart_det_qnty"),
                    price_per_one=info.get("sell__sell_price"),
                    wine_name=info.get("sell__wine__wine_name"),
                    wine_image=info.get("sell__wine__wine_image"),
                )
                dtos.append(dto)
            context["cart_id"] = cart_id

        else:
            logger.error("sell_id cart_id is None")
            return redirect("errorhandling:purchaseError")

        context["dtos"] = dtos
        context["all_price"] = all_price
        logger.info(f"{user_id}: sell_id: {sell_id} cart_id: {cart_id} BuyListView")
        return HttpResponse(template.render(context, request))


class AddPickListView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = request.session.get("memid")
        if user_id is None:
            logger.info("error")
            return redirect("purchaseError")

        else:
            cart_id = get_cart_id(user_id=user_id)
            logger.info(f"{user_id} cart_id: {cart_id} AddPickListView")
            return redirect("purchasing:cartList", cart_id=cart_id)

    def post(self, request):
        user_id = request.POST.get("userId")
        sell_id = request.POST.get("sellId", None)
        quantity = int(request.POST.get("qnty", None))
        current_time = DateFormat(datetime.now()).format("Y-m-d H:i:s")
        print(sell_id)
        try:
            cart_id = add_cart_info(
                user_id=user_id,
                sell_id=sell_id,
                quantity=quantity,
                current_time=current_time,
            )
            logger.info(f"{user_id} sell_id: {sell_id}")
            return redirect("purchasing:cartList", cart_id=cart_id)
        except DatabaseError as db_error:
            logger.error(db_error)
            return redirect("errorhandling:purchaseError")


class PickListView(View):
    def get(self, request, **kwargs):
        user_id = request.session.get("memid")
        cart_id = kwargs.get("cart_id", None)

        page_infos = []
        all_price = 0

        if user_id is None:
            logger.error("NO user_id")
            redirect("purchaseError")
        else:
            print(cart_id)
            if cart_id == 0:
                cart_id = get_cart_id(user_id=user_id)

            elif cart_id != 0:
                cart_state = get_cart_state(cart_id=cart_id)

                if cart_state == -1:
                    logger.error("invaild cart")
                    return redirect("purchaseError")

            page_infos = get_cart_list_page_info(cart_id=cart_id)

            for page_info in page_infos:
                all_price += page_info.get("purchase_price")

            template = loader.get_template("purchasing/pickList.html")
            context = {
                "page_infos": page_infos,
                "all_price": all_price,
                "cart_id": cart_id,
            }
            logger.info(f"{user_id}: cart_id: {cart_id} PickListView")
            return HttpResponse(template.render(context, request))

    def post(self, request, **kwargs):
        request_body = json.loads(request.body)
        cart_detail_id = request_body.get("cartDetailId", None)

        print(cart_detail_id)
        if cart_detail_id is not None:
            detail_cart = WinCartDetail.objects.get(cart_det_id=cart_detail_id)
            detail_cart.delete()
            logger.info(
                f"{request.session['memid']} cart_detail_id: {cart_detail_id} PickListView_DELETE"
            )
            return JsonResponse({"result": "삭제되었습니다"}, status=200)

        else:
            logger.error(
                f"{request.session['memid']} no cart_detail_id or another error PickListView_DELETE"
            )
            return JsonResponse({"result": "문제가 발생했습니다 잠시 후 다시 시도해주세요"}, status=500)


class RemoveBuyList(View):
    @method_decorator(csrf_exempt)
    def post(self, request):
        request_body = json.loads(request.body)
        cart_detail_id = request_body.get("cartDetailId", None)
        if cart_detail_id is not None:
            detail_cart = WinCartDetail.objects.get(cart_det_id=cart_detail_id)
            detail_cart.delete()
            logger.info(
                f"{request.session['memid']} cart_detail_id: {cart_detail_id} RemoveBuyList"
            )
            return JsonResponse({"result": "삭제되었습니다"}, status=200)

        else:
            logger.error(
                f"{request.session['memid']} no cart_detail_id or another error RemoveBuyList"
            )
            return JsonResponse({"result": "문제가 발생했습니다 잠시 후 다시 시도해주세요"}, status=500)


class OrderPageView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = request.session.get("memid")
        template = loader.get_template("purchasing/orderPage.html")
        context = {}
        logger.info(f"{user_id} : OrderPageView")
        return HttpResponse(template.render(context, request))

    def post(self, request):
        template = loader.get_template("purchasing/orderPage.html")

        user_id = request.session.get("memid")
        sell_id = request.POST.getlist("sellId", None)
        quantity = request.POST.getlist("quantity", None)
        purchase_price = request.POST.getlist("purchasePrice", None)
        user_point = request.POST.get("userPoint", None)
        all_price = request.POST.get("allPrice", None)
        cart_id = request.POST.get("cartId", None)
        current_time = DateFormat(datetime.now()).format("Y-m-d H:i:s")

        result = calc(
            user=user_id,
            product_infos=sell_id,
            quantity_per_ones=quantity,
            price_per_ones=purchase_price,
            user_point=int(user_point),
            all_price=int(all_price),
            current_time=current_time,
            cart_info=cart_id,
        )
        # result = sequence.calc()
        if result is None:
            logger.error("No buy list")
            return redirect("purchasing:buyList")
        else:
            try:
                receive_codes = []
                enc_receive_codes = []
                purchase_infos = insert_purchase(result)
                purchase_id = purchase_infos[0]
                purchase_detail_ids = purchase_infos[1]

                for purchase_detail_id in purchase_detail_ids:
                    receive_code = create_receive_code(
                        purchase_num=purchase_detail_id[0]
                    )
                    receive_codes.append(receive_code)
                    enc_receive_code = EncModule().encrypt_receive_code(
                        receive_code=receive_code
                    )
                    queryset = WinReceiveCode(
                        purchase_detail_id=purchase_detail_id[0],
                        receive_code=enc_receive_code,
                    )
                    print(purchase_detail_id)
                    print(purchase_detail_id[0])
                    enc_receive_codes.append(queryset)
                insert_enc_receive_codes(enc_receive_codes)

                detail_infos = get_detail_info(purchase_id)

                for detail_info in detail_infos:
                    receive_code = base64.b64decode(
                        detail_info.get("receive_code")
                    ).decode("utf-8")
                    detail_info["receive_code"] = receive_code
                logger.info(
                    f"{user_id}: purchase_id: {purchase_id} current_time: {current_time} OrderPageView"
                )
            except DatabaseError as db_error:
                logger.error(db_error)
                return redirect("errorhandling:purchaseError")
            context = {"detail_infos": detail_infos}
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
                    print(1)
                    request.session["memid"] = user_id
                    message = 1

                else:
                    print(-1)
                    message = -1

            else:
                print(-2)
                message = -2
        except ObjectDoesNotExist as ex:
            logger.error(ex)
            message = -2

        logger.info(f"{user_id} temp login")
        context = {"message": message}

        return JsonResponse(context, status=200)
