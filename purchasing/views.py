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
    delete_detail_cart_info,
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


logger = logging.getLogger("purchasing")


# Create your views here.
class StoreListView(View):
    """
    "wine/<int:wine_id>/stores"
    """

    def get(self, request, **kwargs):
        """
        사용자가 선택한 와인을 어떤 매장에서 판매하고 있는지를 보여주기 위한 View Class 입니다
        사용자가 선택한 와인의 wine_id를 input값으로 하여 get_store_lists 함수 호출 후
        리턴된 QuerySet을 슬라이싱 해서 front로 리턴함
        """
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
    """
    "wine/<int:wine_id>/stores/<int:page_num>"
    """

    def get(self, request, **kwargs):
        """
        사용자가 선택한 와인을 어떤 매장에서 판매하고 있는지를 보여주기 위한 View Class 입니다
        사용자가 선택한 와인의 wine_id를 input값으로 하여 get_store_lists 함수 호출 후
        리턴된 QuerySet을 슬라이싱 해서 front로 리턴함
        StoreListView 함수와 동일하기 때문에 차후 하나의 코드로 통합할 예정
        """
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
    """
    "sell/<int:sell_id>"
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        csrf token 처리를 위해서 dispatch 함수 overriding
        """
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        사용자가 선택한 매장에서 해당 와인을 얼마에 파는지,
        매장의 상세한 정보는 어떻게 되는지 등을 나타냄
        """

        sell_id = kwargs.get("sell_id", 0)
        user_id = request.session.get("memid")

        template = loader.get_template("purchasing/detailProductInfo.html")

        product_info = get_product_info(sell_id=sell_id)

        if product_info:
            if (
                product_info[0]["store__storeUrl__store_map_url"] == ""
            ):  # store_map_url은 존재하지 않을 수도 있음
                url_value = 0

            else:
                url_value = 1

            product_info = product_info[0]
        else:
            url_value = None  # 에러 페이지로 리다이렉트 시킬 것

        context = {
            "product_info": product_info,
            "url_value": url_value,
            "user_id": user_id,
        }

        logger.info(f"{user_id}: sell_id: {sell_id} DetailProductInfoView")
        return HttpResponse(template.render(context, request))


class ReviewLoadAPI(APIView):
    """
    "sell/<int:sell_id>/reviews"
    """

    def get(self, request, **kwargs):
        """
        해당 상품에 대한 리뷰를 json 형태로 return 함
        select_code는 인자로 넘겨서 정렬 기준을 컨트롤 함
        """

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
    """
    "payment"
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        """
        상품 상세 정보 페이지 - DetailProductInfoView 와
        장바구니 페이지 - PickListView 두 곳에서 넘어오는 경우를 상정하고 if문 분기를 시킴
        PickListView에서 넘어오는 경우 cart_id를 인자로 하여 detail cart list 를 front로 return함
        """

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
    """
    "cart"
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        """
        user/myPage에서 넘어오는 경우 cart_id를 알 수가 없기 때문에 PickListView 앞에서
        현재 사용중인 cart_id를 구하는 역할을 함
        """
        user_id = request.session.get("memid")
        if user_id is None:
            logger.info("error")
            return redirect("purchaseError")

        else:
            cart_id = get_cart_id(user_id=user_id)
            logger.info(f"{user_id} cart_id: {cart_id} AddPickListView")
            return redirect("purchasing:cartList", cart_id=cart_id)

    def post(self, request):
        """
        DetailProductInfoView에서 장바구니에 추가하고자 하는 상품과 그 갯수를 db에 저장하고
        cart_id를 반환하여 PickListView로 이동시킴
        """
        user_id = request.POST.get("userId")
        sell_id = request.POST.get("sellId", None)
        quantity = int(request.POST.get("qnty", None))
        current_time = DateFormat(datetime.now()).format("Y-m-d H:i:s")
        try:
            cart_id = add_cart_info(
                user_id=user_id,
                sell_id=sell_id,
                quantity=quantity,
                current_time=current_time,
            )

            logger.info(f"{user_id} sell_id: {sell_id}")
            return redirect("purchasing:cartList", cart_id=cart_id)

        except DatabaseError as ex:
            logger.error(ex)
            return redirect("errorhandling:purchaseError")


class PickListView(View):
    """
    "cart/<int:cart_id>"
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        키워드 인수로 전달받은 cart_id를 통해 현재 존재하는 장바구니 정보를 front로 return함
        """
        user_id = request.session.get("memid")
        cart_id = kwargs.get("cart_id", None)
        page_infos = []
        all_price = 0
        

        if user_id is None:
            logger.error("NO user_id")
            redirect("purchaseError")
        else:
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
        """
        json으로 전달받은 cart_detail_id를 통해 해당하는 상품을 장바구니 목록에서 삭제함
        자후 delete 함수로 바꾸고 serializer 적용 예정
        """
        request_body = json.loads(request.body)
        cart_detail_id = request_body.get("cartDetailId", None)
        print(cart_detail_id)
        if cart_detail_id is not None:
            result = delete_detail_cart_info(cart_det_id=cart_detail_id)
            logger.info(
                f"{request.session['memid']} cart_detail_id: {result} RemoveBuyList"
            )
            return JsonResponse({"result": "삭제되었습니다"}, status=200)

        else:
            logger.error(
                f"{request.session['memid']} no cart_detail_id or another error RemoveBuyList"
            )
            return JsonResponse({"result": "문제가 발생했습니다 잠시 후 다시 시도해주세요"}, status=500)


class RemoveBuyList(View):
    """
    "remove-buy-list"
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        json으로 전달받은 cart_detail_id를 통해 해당하는 상품을 장바구니 목록에서 삭제함
        자후 delete 함수로 바꾸고 serializer 적용 예정
        """
        request_body = json.loads(request.body)
        cart_detail_id = request_body.get("cartDetailId", None)
        if cart_detail_id is not None:
            result = delete_detail_cart_info(cart_det_id=cart_detail_id)
            logger.info(
                f"{request.session['memid']} cart_detail_id: {result} RemoveBuyList"
            )
            return JsonResponse({"result": "삭제되었습니다"}, status=200)

        else:
            logger.error(
                f"{request.session['memid']} no cart_detail_id or another error RemoveBuyList"
            )
            return JsonResponse({"result": "문제가 발생했습니다 잠시 후 다시 시도해주세요"}, status=500)


class OrderPageView(View):
    """
    "order"
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        """
        해당 함수 실사용 환경에서 호출되는지 확인 못함
        추후 확인 후 호출되지 않으면 삭제 예정
        """

        user_id = request.session.get("memid")
        template = loader.get_template("purchasing/orderPage.html")
        context = {}
        logger.info(f"{user_id} : OrderPageView")
        return HttpResponse(template.render(context, request))

    def post(self, request):
        """
        장바구니 목록 결제와 상품 상세 페이지에서 바로 결제하는 경우 두 가지 전부 대응할 수 있도록 calc 함수 정의 후 사용
        수령코드 생성 후 base64로 인코딩 해서 db에 저장, 인코딩 하지 않은 데이터는 front로 리턴
        """

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
                    enc_receive_codes.append(enc_receive_code)

                insert_enc_receive_codes(
                    enc_receive_codes=enc_receive_codes,
                    purchase_detail_ids=purchase_detail_ids,
                )

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
