import json
from datetime import datetime
import logging
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import loader
from django.http.response import HttpResponse, JsonResponse
from django.utils.dateformat import DateFormat
from django.db.utils import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from store.db_access.query_set import (
    PageSerializer,
    ProductListSerializer,
    PurchaseDetailSerializer,
    delete_user_info,
    get_product_list,
    get_reviews_by_seller,
    insert_store_info,
    insert_sell_info,
    delete_store_info,
    check_store_product_info,
    check_store_regist_number,
    get_store_info,
    get_detail_sell_list,
    get_product_list_by_seller,
    delete_product,
    check_passwd,
    drop_store_info,
    get_store_revenue,
    search_product_list,
    search_receive_code,
    update_purchase_det_state,
)
from purchasing.usecase.receive_code_create_enc_module import EncModule
from store.usecase.pagination import db_preprocessing, pagenation

# Create your views here.

# 일반 정보 입력 후 매장 정보 등록
# user 회원가입에서 넘어온다.
# temp_id 는 회원가입 시 입력한 id이고, 점주 회원가입이 모두 끝날 때 까지 전달, 보존하고 파기한다.
# temp_id 를 GET이 아닌 session으로부터 받는다.

logger = logging.getLogger("store")


class StoreRegistrationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = request.session.get("temp_id")
        info = check_store_product_info(user_id=user_id)

        if info:
            logger.error("already have store")
            return redirect("storeMyPage")

        else:
            template = loader.get_template("store/storeRegistration.html")
            context = {"user_id": user_id}
            logger.info(f"{user_id} StoreRegistrationView")
            return HttpResponse(template.render(context, request))

    # storeRegistration.html
    # storeRegistrationScript.js 를 import 한다.
    # storeRegistrationScript.js에서 입력값에 대한 유효성 검사, 위치 url API 를 import 했다.

    def post(self, request):
        user_id = request.POST.get("userId", None)
        store_regist = request.POST.get("btnStoreRegist", None)
        back = request.POST.get("btnBack", None)

        # 파이썬에서도 정규식 검증하고 db insert하기
        if store_regist:
            main_address = request.POST.get("mainAddress", None)
            detail_address = request.POST.get("detailAddress", None)
            store_name = request.POST.get("storeName", None)
            store_reg_num = request.POST.get("storeRegNum", None)
            store_email = request.POST.get("storeEmail")
            store_map_url = request.POST.get("storeMapUrl", None)
            store_address = main_address + "@" + detail_address

            try:
                insert_store_info(
                    user_id=user_id,
                    store_address=store_address,
                    store_name=store_name,
                    store_reg_num=store_reg_num,
                    store_email=store_email,
                    store_map_url=store_map_url,
                )

            except DatabaseError as ex:
                logger.error(ex)
                redirect("errorhandling:storeError")

            logger.info(f"{user_id}: store_name: {store_name} StoreRegistrationView")
            return redirect("productAddition")

        elif back:
            logger.info(f"{user_id}:  back StoreRegistrationView")
            delete_user_info(user_id=user_id)
            return redirect("inputStore")

    # insert_store_info 라는 함수를 정의하여 사용했다.


class CheckStoreRegistNumberView(View):
    def get(self, request, **kwargs):
        reg_num = kwargs.get("regnum", None)
        print(reg_num)
        if reg_num is None:
            logger.error("No reg_num CheckStoreRegistNumberView")
            return JsonResponse({"result": "문제가 발생했습니다 잠시 후 다시 시도해주세요"}, status=500)

        else:
            result = check_store_regist_number(reg_num=reg_num)

            if result is True:
                logger.info(f"{reg_num} CheckStoreRegistNumberView")
                return JsonResponse(
                    {"result": "유효한 사업자 등록번호입니다", "code": "1"}, status=200
                )

            else:
                logger.info(f"{reg_num} CheckStoreRegistNumberView")
                return JsonResponse(
                    {"result": "이미 등록된 사업자 등록번호입니다", "code": "-1"}, status=200
                )

    # js/productAdditionScript.js 를 import
    #


class ProductAdditionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request, **kwargs):
        modify = kwargs.get("mdfy", None)
        user_id = request.session.get("temp_id")

        if user_id is None:
            user_id = request.session.get("memid")

        if modify == "mdfy":
            modify = 1
        else:
            modify = 0

        page_num = 1
        show_length = 20
        end = int(show_length) * int(page_num)
        start = end - show_length
        result = get_product_list()
        list_info = db_preprocessing(db_data=result, end_page=end, start_page=start)
        paging_result = pagenation(
            show_length=show_length,
            page_num=page_num,
            end_page=end,
            start_page=start,
            datas=list_info,
        )
        pages_count = paging_result["pages_count"]
        db_data = paging_result["db_data"]
        state = paging_result["pages_count"]
        product_list = get_product_list_by_seller(user_id=user_id)
        store_id = get_store_info(user_id=user_id)["store_id"]

        # 이미 등록된 상품 리스트들도 페이징 처리 할 것
        template = loader.get_template("store/productAddition.html")
        context = {
            "wines": db_data,
            "store_id": store_id,
            "product_list": product_list,
            "modify": modify,
            "pages_count": pages_count,
            "next": pages_count[-1] + 1,
        }
        logger.info(f"{user_id}: ProductAdditionView")
        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = request.session.get("temp_id")
        if user_id is None:
            user_id = request.session.get("memid")
        store_id = request.POST.get("storeId", None)
        sell_ids = request.POST.getlist("sellId", None)
        wine_ids = request.POST.getlist("wineId", None)
        sell_prices = request.POST.getlist("sellPrice", None)
        sell_promots = request.POST.getlist("sellPromot", None)
        sell_state = 1
        btn_cancel_regist = request.POST.get("btnCancelRegist", None)
        btn_product_add = request.POST.get("btnProductAdd", None)
        btn_back = request.POST.get("btnBackRegist", None)
        current_time = DateFormat(datetime.now()).format("Y-m-d H:i:s")

        if btn_product_add is not None:
            print("product add")
            try:
                insert_sell_info(
                    user_id,
                    store_id,
                    wine_ids,
                    current_time,
                    sell_ids,
                    sell_prices,
                    sell_promots,
                    sell_state,
                )
                if request.session.get("memid"):
                    logger.info(
                        f"{user_id}: wine_ids: {wine_ids} ProductAdditionView append sell_list"
                    )
                    return redirect("sellList", page_num=1)
                else:
                    logger.info(
                        f"{user_id}: wine_ids: {wine_ids} ProductAdditionView insert sell_list"
                    )
                    return redirect("login")
            except DatabaseError as ex:
                logger.error(ex)
                return redirect("errorhandling:storeError")

        elif btn_cancel_regist is not None:
            logger.info(f"{user_id}: ProductAdditionView btn_cancel_regist")
            delete_store_info(store_id=store_id)
            return redirect("login")

        elif btn_back is not None:
            logger.info(f"{user_id}: ProductAdditionView btn_back")
            delete_store_info(store_id=store_id)
            return redirect("storeRegistration")


class ProductListView(APIView):
    def get(self, request, **kwargs):
        user_id = request.session.get("memid", None)
        if user_id is None:
            user_id = request.session.get("temp_id", None)
        page_num = kwargs.get("page_num", 1)
        search_keyword = request.GET.get("srhkeyword", None)

        show_length = 20
        end = int(show_length) * int(page_num)
        start = end - show_length
        if search_keyword is not None:
            wines = search_product_list(search_keyword=search_keyword)
        else:
            wines = get_product_list()

        list_info = db_preprocessing(db_data=wines, end_page=end, start_page=start)
        paging_result = pagenation(
            show_length=show_length,
            page_num=page_num,
            end_page=end,
            start_page=start,
            datas=list_info,
        )
        pages = {}

        pages["pages"] = paging_result["pages_count"]
        print(pages)
        serializer = ProductListSerializer(
            paging_result["db_data"],
            many=True,
        ).data
        page_serializer = PageSerializer(pages, context={"wines": serializer})

        json_result = JSONRenderer().render(page_serializer.data)
        logger.info(f"{user_id} : search_keyword: {search_keyword} ProductListView")
        return Response(json_result)


class DiscontinueProductView(View):
    def get(self, request):
        user_id = request.session.get("memid")
        wine_id = request.GET.get("wineid", None)
        print(wine_id)
        delete_product(wine_id=wine_id, user_id=user_id)
        logger.info(f"{user_id}: wine_id: {wine_id} DiscontinueProductView")
        return JsonResponse({"result": "삭제되었습니다"}, status=200)


class StoreMyPageView(View):
    def get(self, request):
        user_id = request.session.get("memid")
        template = loader.get_template("store/storeMyPage.html")
        context = {"user_id": user_id}
        logger.info(f"{user_id}: StoreMyPageView")
        return HttpResponse(template.render(context, request))


class SearchReceiveCodeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("store/searchReceiveCode.html")
        user_id = request.session.get("memid")
        logger.info(f"{user_id}: SearchReceiveCodeView")
        context = {"result": ""}

        return HttpResponse(template.render(context, request))

    def post(self, request):
        purchase_detail_id = request.POST.get("purchaseDetailId", None)
        template = loader.get_template("store/searchReceiveCode.html")
        user_id = request.session.get("memid")
        update_purchase_det_state(purchase_detail_id=purchase_detail_id)

        logger.info(
            f"{user_id}: purchase_detail_id: {purchase_detail_id} SearchReceiveCodeView"
        )
        context = {"result": "수령 처리가 완료되었습니다", "result2": "다음 "}

        return HttpResponse(template.render(context, request))

    # 수령코드 get 방식으로 검색


class SearchReceiveCodeApi(APIView):
    def get(self, request, **kwargs):
        receive_code = kwargs.get("code", None)
      
        if receive_code is not None:
            receive_code = receive_code.replace(" ", "")
        else:
            receive_code = "None"
        result = search_receive_code(
            receive_code=EncModule().encrypt_receive_code(receive_code)
        )
        serializer = PurchaseDetailSerializer(result)
        json_result = JSONRenderer().render(serializer.data)
        logger.info(f"{request.session['memid']}: receive_code: {receive_code}")
        return Response(json_result)


class StoreInfoView(View):
    def get(self, request):
        template = loader.get_template("store/storeInfo.html")
        user_id = request.session.get("memid")
        info = get_store_info(user_id=user_id)
        full_address = info.get("store_address").split("@")
        main_address = full_address[0]
        detail_address = full_address[1]

        context = {
            "info": info,
            "main_address": main_address,
            "detail_address": detail_address,
        }
        logger.info(f"{request.session['memid']}: StoreInfoView")
        return HttpResponse(template.render(context, request))

        # get_store_info : user_id 가 같은 모든 row를 select한다. 가장 최근의 row를 선택하기 위해 [0]을 붙인다.
        # split 은 주어진 문자열을 기준으로 list로 나눈다.


class StoreInfoModificationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("store/storeInfoModification.html")
        user_id = request.session.get("memid")
        info = get_store_info(user_id=user_id)
        full_address = info.get("store_address").split("@")
        main_address = full_address[0]
        detail_address = full_address[1]

        context = {
            "info": info,
            "main_address": main_address,
            "detail_address": detail_address,
        }
        logger.info(f"{request.session['memid']}: StoreInfoModificationView")
        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = request.session.get("memid")
        main_address = request.POST.get("mainAddress", None)
        detail_address = request.POST.get("detailAddress", None)
        store_name = request.POST.get("storeName", None)
        store_reg_num = request.POST.get("storeRegNum", None)
        store_email = request.POST.get("storeEmail")
        store_map_url = request.POST.get("storeMapUrl", None)

        store_address = main_address + "@" + detail_address
        # 파이썬에서도 정규식 검증하고 db insert하기

        try:
            insert_store_info(
                user_id=user_id,
                store_address=store_address,
                store_name=store_name,
                store_reg_num=store_reg_num,
                store_email=store_email,
                store_map_url=store_map_url,
            )

        except DatabaseError as ex:
            logger.error(ex)
            redirect("errorhandling:storeError")

        logger.info(f"{user_id}: StoreInfoModificationView")
        return redirect("storeInfo")


class SellDetailListView(View):
    def get(self, request, **kwargs):
        user_id = request.session.get("memid")
        page_num = kwargs.get("pageNum", 1)
        template = loader.get_template("store/sellDetailList.html")
        show_length = 30
        end = int(show_length) * int(page_num)
        start = end - 30
        detail_sell_list = get_detail_sell_list(user_id=user_id)
        list_info = db_preprocessing(
            db_data=detail_sell_list, end_page=end, start_page=start
        )
        pagination_result = pagenation(
            show_length=show_length,
            page_num=page_num,
            end_page=end,
            start_page=start,
            datas=list_info,
        )
        db_data = pagination_result["db_data"]
        pages_count = pagination_result["pages_count"]
        print(pages_count)
        context = {"list": db_data, "pages_count": pages_count}
        logger.info(f"{user_id}: page_num: {page_num} SellDetailListView")
        return HttpResponse(template.render(context, request))


class SellMerchandiseView(View):
    def get(self, request, **kwargs):
        page_num = kwargs.get("page_num", 1)
        show_length = 30
        end = int(show_length) * int(page_num)
        start = end - 30

        user_id = request.session.get("memid")

        product_list = get_product_list_by_seller(user_id=user_id)
        list_info = db_preprocessing(
            db_data=product_list, end_page=end, start_page=start
        )
        paging_result = pagenation(
            show_length=show_length,
            page_num=page_num,
            end_page=end,
            start_page=start,
            datas=list_info,
        )

        db_data = paging_result["db_data"]
        pages_count = paging_result["pages_count"]

        template = loader.get_template("store/productList.html")
        context = {"product_list": db_data, "pages_count": pages_count}

        logger.info(f"{user_id}: page_num: {page_num} SellMerchandiseView")
        return HttpResponse(template.render(context, request))


class DropStoreView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("store/dropStore.html")
        context = {}
        logger.info(f"{request.session['memid']}: DropStoreView")
        return HttpResponse(template.render(context, request))

    def post(self, request):
        passwd = json.loads(request.body).get("passwd", None)
        user_id = request.session.get("memid")
        result = check_passwd(user_id=user_id, passwd=passwd)

        if result == 0:
            text = "비밀번호가 다릅니다"
            code = -1

        elif result == 1:
            try:
                drop_store_info(user_id=user_id)
                text = "등록된 점포가 삭제 되었습니다"
                code = 1
            except Exception as ex:
                text = "문제가 발생했습니다 잠시 후 다시 시도해주세요"
                code = -1
                logger.error(ex)
                return JsonResponse({"result": text, "code": code}, status=500)

        logger.info(f"{request.session['memid']}: passwd: {passwd} DropStoreView")
        return JsonResponse({"result": text, "code": code}, status=200)


class StoreRevenueMainView(View):
    def get(self, request, **kwargs):
        page_num = kwargs.get("page_num", 1)
        user_id = request.session.get("memid")
        template = loader.get_template("store/storeRevenueMain.html")
        show_length = 30
        end = int(show_length) * int(page_num)
        start = end - 30
        revenue_info = get_store_revenue(user_id=user_id)
        list_info = db_preprocessing(
            db_data=revenue_info, end_page=end, start_page=start
        )
        paging_result = pagenation(
            show_length=show_length,
            page_num=page_num,
            end_page=end,
            start_page=start,
            datas=list_info,
        )
        db_data = paging_result["db_data"]
        pages_count = paging_result["pages_count"]
        context = {"revenue_info": db_data, "pages_count": pages_count}

        logger.info(f"{user_id}: StoreRevenueMainView")
        return HttpResponse(template.render(context, request))


class StoreRevenueTermView(View):
    def get(self, request):
        user_id = request.session.get("memid")
        term = int(request.GET.get("term", 0))
        print(term)
        revenue_info = list(get_store_revenue(user_id=user_id, term=term))
        print(revenue_info)

        logger.info(f"{user_id}: term: {term} StoreRevenueTermView")
        return JsonResponse({"result": revenue_info}, status=200)


class StoreReviewView(View):
    def get(self, request, **kwargs):
        sell_id = kwargs.get("sell_id")
        page_num = kwargs.get("page_num", 1)
        template = loader.get_template("store/storeShowReviews.html")
        show_length = 30
        end = int(show_length) * int(page_num)
        start = end - 30
        reviews = get_reviews_by_seller(sell_id=sell_id)
        list_info = db_preprocessing(db_data=reviews, end_page=end, start_page=start)
        paging_result = pagenation(
            show_length=show_length,
            page_num=page_num,
            end_page=end,
            start_page=start,
            datas=list_info,
        )
        db_data = paging_result["db_data"]
        pages_count = paging_result["pages_count"]
        context = {"reviews": db_data, "pages_count": pages_count}

        logger.info(f"{request.session['memid']}: sell_id: {sell_id} StoreReviewView")
        return HttpResponse(template.render(context, request))
