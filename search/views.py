from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from detail.models import WinWine, WinWineRegion, WinDetailView, WinDetailViewN
from django.db.models import Q
import difflib
from search.models import WinSearch, WinSearchN, WinRecommend
from _datetime import datetime
from django.utils.dateformat import DateFormat
from user.models import WinUser, WinUserFavorite, WinReview
from purchasing.models import WinPurchaseDetail
from store.models import WinSell
from django.db.models import F
from search.functions.functions import (
    win_corr_code,
    win_corr_cap,
    win_corr_alc,
    win_reco_alc,
    win_reco_color,
    win_reco_food,
    win_reco_taste,
    win_corr_alc_inverse,
    sort,
    list_corr_5,
    list_corr_6,
    list_corr_2d,
    random_generate,
)
from django.db.models.aggregates import Count, Avg
import random
import numpy as np
from numpy.f2py.crackfortran import get_sorted_names
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



class SearchByNameView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("search/main.html")  # 메인 페이지이자 검색 페이지
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        name_language = request.POST.get("namelanguage")  # 사용자가 선택한 검색 입력 언어
        search_word = request.POST.get("searchname")  # 사용자가 입력한 검색어 텍스트
        template = loader.get_template("search/searchByNameList.html")

        # DB에서 목록 불러오기

        if name_language == "winenamekor":  # if 와인 이름 (국문)
            start_results = WinWine.objects.filter(
                wine_name__startswith=search_word
            )  # SEARCH_QUERY_01 (와인 이름이 검색어로 시작하는 것 select)
            start_results_count = (
                start_results.count()
            )  # SEARCH_QUERY_02 (select한 queryset의 row 개수)

            include_results = WinWine.objects.filter(
                ~Q(wine_name__startswith=search_word), wine_name__contains=search_word
            )  # SEARCH_QUERY_03 (와인 이름에 검색어가 포함된 것 select)
            include_results_count = (
                include_results.count()
            )  # SEARCH_QUERY_04 (select한 queryset의 row 개수)

        elif name_language == "winenameeng":  # if 와인 이름 (영문)
            start_results = WinWine.objects.filter(
                wine_name_eng__istartswith=search_word
            )  # SEARCH_QUERY_05 (와인 이름이 검색어로 시작하는 것 select (대소문자 구분하지 않는다))
            start_results_count = (
                start_results.count()
            )  # SEARCH_QUERY_06 (select한 queryset의 row 개수)

            include_results = WinWine.objects.filter(
                ~Q(wine_name_eng__istartswith=search_word),
                wine_name_eng__icontains=search_word,
            )  # SEARCH_QUERY_07 (와인 이름에 검색어가 포함된 것 select (대소문자 구분하지 않는다))
            include_results_count = (
                include_results.count()
            )  # SEARCH_QUERY_08 (select한 queryset의 row 개수)

        results_count = (
            start_results_count + include_results_count
        )  # 회원 조회수와 비회원 조회수의 합

        # 검색어 수집

        # 사용자가 회원일 때
        if request.session.get("memid"):
            search_rec = WinSearch(
                user_id=request.session.get("memid"),
                search_word=search_word,
                search_time=DateFormat(datetime.now()).format("Y-m-d h:i:s"),
            )
            search_rec.save()  # SEARCH_QUERY_09 (회원 id와 검색입력 정보 수집)

        # 사용자가 비회원일 때
        else:
            search_n_rec = WinSearchN(
                search_n_word=search_word,
                search_n_time=DateFormat(datetime.now()).format("Y-m-d h:i:s"),
            )
            search_n_rec.save()  # SEARCH_QUERY_10 (비회원의 검색입력 정보 수집)

        start_paginator = Paginator(start_results, 10)
        page = request.GET.get("page")

        try:
            page_obj = start_paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_obj = start_paginator.page(page)
        except EmptyPage:
            page = start_paginator.num_pages
            page_obj = start_paginator.page(page)

        left_index = int(page) - 2
        if left_index < 1:
            left_index = 1

        right_index = int(page) + 2

        if right_index > start_paginator.num_pages:
            right_index = start_paginator.num_pages

        custom_range = range(left_index, right_index + 1)

        #
        #
        # recommend_list = []
        # for r in start_results:
        #     print(r.wine_id)
        #     recommend_list.append(r.wine_id)
        # for r in include_results:
        #     print(r.wine_id)
        #     recommend_list.append(r.wine_id)
        #
        # print(recommend_list)
        #
        # if len(recommend_list) < 7 :
        #     recommend_list = random.sample(recommend_list, len(recommend_list))
        # else :
        #     recommend_list = random.sample(recommend_list, 6)
        #
        #
        #
        # print(recommend_list)

        context = {  # 검색어, 검색 결과(첫글자), 검색 결과(포함), 결과 수
            "search_word": search_word,
            "start_results": start_results,
            "include_results": include_results,
            "results_count": results_count,
            "page_obj": page_obj,
            "start_paginator": start_paginator,
            "custom_range": custom_range,
        }

        return HttpResponse(template.render(context, request))


class ShowRelateKeyword(APIView):
    def get(self, request):
        search_word = request.GET.get("searchword", None)
        name_language = request.GET.get("namelanguage", None)
        result = {}
        if name_language == "winenamekor":
            result = (
                WinWine.objects.annotate(result=F("wine_name"))
                .filter(wine_name__icontains=search_word, wine_name__range=("가", "힣"))
                .values("result")[:8]
            )
            serialize = SearchResultSerializer(result, many=True)

        elif name_language == "winenameeng":
            result = (
                WinWine.objects.annotate(result=F("wine_name_eng"))
                .filter(wine_name_eng__icontains=search_word)
                .values("result")[:8]
            )
            serialize = SearchResultSerializer(result, many=True)

        json_result = JSONRenderer().render(serialize.data)
        return Response(json_result)


class SearchResultSerializer(serializers.Serializer):
    result = serializers.CharField()


class SearchByCategoryView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("search/searchByCategory.html")  # 카테고리 검색 페이지
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        template = loader.get_template(
            "search/searchByCategoryList.html"
        )  # 카테고리 검색 결과 페이지

        # 사용자로부터 받는 입력

        list_kind = list(map(int, request.POST.getlist("winekind")))
        list_capacity = list(map(int, request.POST.getlist("winecapacity")))
        alc_min = float(request.POST.getlist("alcmin")[0])
        alc_max = float(request.POST.getlist("alcmax")[0])
        # list_alc = list(map(int, request.POST.getlist("winealc")))
        list_dangdo = list(map(int, request.POST.getlist("dangdo")))
        list_sando = list(map(int, request.POST.getlist("sando")))
        list_tannin = list(map(int, request.POST.getlist("tannin")))
        list_food = list(map(int, request.POST.getlist("winefood")))
        list_region = list(map(int, request.POST.getlist("wineregion")))

        # getlist 로 checkbox 의 여러 값을 리스트로 받는다.
        # 리스트 성분들을 전부 문자열로 받기 때문에 숫자로 변환해야한다. map(함수, 리스트) 로 리스트 성분에 함수를 적용한다.
        # 함수를 적용한 성분들을 다시 성분으로 하는 리스트를 얻는다.

        print(list_kind)
        print(alc_min)
        print(alc_max)
        print(list_dangdo)
        print(list_sando)
        print(list_tannin)
        print(list_food)
        print(list_region)
        print(list_capacity)

        # 함수 적용                                         # ORM의 filter에서 쓸 값들을 정하기 위한 함수
        list_kind = list_corr_5(list_kind)
        list_dangdo = list_corr_5(list_dangdo)
        list_sando = list_corr_5(list_sando)
        list_tannin = list_corr_5(list_tannin)
        list_food = list_corr_5(list_food)
        list_region = list_corr_6(list_region)
        # list_alc = list(map(list_corr_2d, list_alc))

        print(list_kind)
        # print(list_alc)
        print(list_dangdo)
        print(list_sando)
        print(list_tannin)
        print(list_food)
        print(list_region)
        print(list_capacity)

        # DB에서 목록 불러오기

        # SEARCH_QUERY_11
        if list_capacity == [750]:
            category_results = WinWine.objects.filter(
                wine_sort__in=list_kind,
                # wine_alc__in = list( float, list_alc ),
                wine_alc__gt=alc_min,
                wine_alc__lt=alc_max,
                wine_dangdo__in=list_dangdo,
                wine_sando__in=list_sando,
                wine_tannin__in=list_tannin,
                wine_food__in=list_food,
                wine_region__in=list_region,
                wine_capacity=750,
            ).select_related("wine_region")
            print("750")

        # SEARCH_QUERY_12
        elif list_capacity == [0]:
            category_results = WinWine.objects.filter(
                (~Q(wine_capacity=750)),
                wine_sort__in=list_kind,
                # wine_alc__in = list( float, list_alc ),
                wine_alc__gt=alc_min,
                wine_alc__lt=alc_max,
                wine_dangdo__in=list_dangdo,
                wine_sando__in=list_sando,
                wine_tannin__in=list_tannin,
                wine_food__in=list_food,
                wine_region__in=list_region,
                wine_capacity__gt=0,
            ).select_related("wine_region")
            print("0")

        # SEARCH_QUERY_13
        else:
            category_results = WinWine.objects.filter(
                wine_sort__in=list_kind,
                # wine_alc__in = list( float, list_alc ),
                wine_alc__gt=alc_min,
                wine_alc__lt=alc_max,
                wine_dangdo__in=list_dangdo,
                wine_sando__in=list_sando,
                wine_tannin__in=list_tannin,
                wine_food__in=list_food,
                wine_region__in=list_region,
            ).select_related("wine_region")
            print("그 외")

        print(category_results)


        results_count = category_results.count()  # 결과 개수
        context = {
            "list_kind": list(map(win_corr_code, list_kind)),
            "list_capacity": list(map(win_corr_cap, list_capacity)),
            "list_dangdo": list(map(win_corr_code, list_dangdo)),
            "list_sando": list(map(win_corr_code, list_sando)),
            "list_tannin": list(map(win_corr_code, list_tannin)),
            "list_food": list(map(win_corr_code, list_food)),
            "list_region": list(map(win_corr_code, list_region)),
            "category_results": category_results,
            "results_count": results_count,
        }

        return HttpResponse(template.render(context, request))


class SearchByUserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = request.session.get("memid")
        user = WinUser.objects.get(user_id=user_id)
        print(user)
        user_grade = user.user_grade.user_grade
        print(user_grade)
        template = loader.get_template("search/searchByUser.html")
        context = {
            "user_grade" : user_grade
            }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        # 회원 id 불러오기
        user_id = request.session.get("memid")
        user = WinUser.objects.get(user_id=user_id)
        print(user_id)
        print(user)
        
        user_exist = True
        
        try:
            recommend_dto = WinRecommend.objects.get(user_id=user_id)
        except WinRecommend.DoesNotExist : 
            user_exist = False
            
        print(user_exist)
        
        
        if (user_exist):
            # recommend_table 에서 불러오기 
            recommend_dto = WinRecommend.objects.get(user_id=user_id)
            print(recommend_dto)
    
            recommend_list = []
            recommend_list.append(recommend_dto.recommend_rank_1)
            recommend_list.append(recommend_dto.recommend_rank_2)
            recommend_list.append(recommend_dto.recommend_rank_3)
            recommend_list.append(recommend_dto.recommend_rank_4)
            recommend_list.append(recommend_dto.recommend_rank_5)
            recommend_list.append(recommend_dto.recommend_rank_6)
            recommend_list.append(recommend_dto.recommend_rank_7)
            recommend_list.append(recommend_dto.recommend_rank_8)
            recommend_list.append(recommend_dto.recommend_rank_9)
            recommend_list.append(recommend_dto.recommend_rank_10)
            print(recommend_list)
            
            wine_dtos = WinWine.objects.only(
                "wine_id",
                "wine_name",
                "wine_name_eng",
                "wine_image",
            ).order_by("wine_id")
            results_count = wine_dtos.count()
            print(results_count)
            
             
            sorted_id = []
            sorted_name = []
            sorted_name_eng = []
            sorted_image = []
            
            for idx in recommend_list:
                sorted_id.append(wine_dtos[int(idx)].wine_id)
                sorted_name.append(wine_dtos[int(idx)].wine_name)
                sorted_name_eng.append(wine_dtos[int(idx)].wine_name_eng)
                sorted_image.append(wine_dtos[int(idx)].wine_image)
            
            # Template 에서 반복문을 쓰기 위해 zip으로 묶는다
            list_for_user = zip(sorted_id, sorted_name, sorted_name_eng, sorted_image)
            
            print(sorted_id)
            print(sorted_name)
            print(sorted_image)
            print(len(sorted_id))
            print(len(sorted_name))
            print(len(sorted_name_eng))
            print(len(sorted_image))
            print(results_count)
            
            recommend_by_user = 1
    
        else : 
            
            # 회원 취향 정보 불러오기
            fav_dto = WinUserFavorite.objects.get(user_id=user.user_id)
            user_favorite = [
                fav_dto.fav_wine_color,
                fav_dto.fav_alc,
                fav_dto.fav_sweet,
                fav_dto.fav_bitter,
                fav_dto.fav_sour,
                fav_dto.fav_food,
            ]
            print(user_favorite)
            
            # 우선순위별 가중치 점수 부여하기 
            arr = [0.05]
            user_prior = arr * 6
            user_prior[fav_dto.fav_first_priority - 1] += 0.45
            user_prior[fav_dto.fav_second_priority - 1] += 0.20
            user_prior[fav_dto.fav_third_priority - 1] += 0.05
            print(user_prior)
            wine_rearrange = []
            dto_list = []
    
            # 와인 정보 불러오기 
            wine_dtos = WinWine.objects.only(
                "wine_id",
                "wine_name",
                "wine_image",
                "wine_sort",
                "wine_alc",
                "wine_dangdo",
                "wine_sando",
                "wine_tannin",
                "wine_food",
            ).order_by("wine_id")
            results_count = wine_dtos.count()
            print(results_count)
    
            # 회원 취향과 와인 특성 매칭해서 각 항목별 점수 얻기 (회원 : 1명, 와인 N개  총 N번 반복)
            for wine_dto in wine_dtos:
                color_score = win_reco_color(user_favorite[0], wine_dto.wine_sort)
                alc_score = win_reco_alc(
                    user_favorite[1], win_corr_alc_inverse(wine_dto.wine_alc)
                )
                sweet_score = win_reco_taste(user_favorite[2], wine_dto.wine_dangdo)
                bitter_score = win_reco_taste(user_favorite[3], wine_dto.wine_tannin)
                sour_score = win_reco_taste(user_favorite[4], wine_dto.wine_sando)
                food_score = win_reco_food(user_favorite[5], wine_dto.wine_food)
    
                # 각 항목별 점수 총합 
                user_similarity = (
                    color_score * user_prior[0]
                    + alc_score * user_prior[1]
                    + sweet_score * user_prior[2]
                    + bitter_score * user_prior[3]
                    + sour_score * user_prior[4]
                    + food_score * user_prior[5]
                )
                # print([color_score, alc_score, sweet_score, bitter_score, sour_score, food_score])
                # print([user_prior[0], user_prior[1], user_prior[2], user_prior[3], user_prior[4], user_prior[5]])
                # print(user_similarity)
                
                # 빈 리스트에 append하여 와인 id 순서대로 유사도 나열
                wine_rearrange.append(user_similarity)
                
                # 와인 id를 기존 순서대로 빈 리스트에 나열 
                dto_list.append(wine_dto.wine_id)
    
            # print( len(wine_rearrange))
            print(dto_list)
            print()
            print(wine_rearrange)
            
            
            
            wine_rearrange = np.array(wine_rearrange)                   # 유사도 리스트를 numpy 포맷으로 변환
            sorted_wine_id = np.argsort(wine_rearrange)[::-1]           # 유사도 리스트를 내림차순으로 정렬하여 index를 반환
            #sorted_wine_id = np.add(sorted_wine_id, 1)
            #sorted_wine_id_100 = sorted_wine_id[0:99]
            sorted_id = []                                              # 유사도 내림차순으로 정렬된 와인 id 빈 리스트                                            
            sorted_name = []                                            # 유사도 내림차순으로 정렬한 와인 이름 빈 리스트 
            sorted_name_eng = []     
            sorted_image = []                                           # 유사도 내림차순으로 정렬한 와인 이미지 빈 리스트 
            # for idx in sorted_wine_id:
            #     list_for_user.append(wine_dtos[idx])
                
              
                
            # search_rearrange = sort(wine_rearrange, dto_list)
            #
            #print(sorted_wine_id_100)
            
            print(wine_dtos)
            print()
            print(sorted_wine_id)
            print(max(sorted_wine_id))
            print(min(sorted_wine_id))
            print(wine_dtos[1].wine_name)  
            
            # 세 리스트에 유사도 내림차순으로 정렬
            for idx in sorted_wine_id : 
                sorted_id.append(wine_dtos[int(idx)].wine_id)
                sorted_name.append(wine_dtos[int(idx)].wine_name)
                sorted_name_eng.append(wine_dtos[int(idx)].wine_name_eng)
                sorted_image.append(wine_dtos[int(idx)].wine_image)
            
            sorted_id = sorted_id[:10]
            sorted_name = sorted_name[:10]
            sorted_name_eng = sorted_name_eng[:10]
            sorted_image = sorted_image[:10]
            
            # Template 에서 반복문을 쓰기 위해 zip으로 묶는다
            list_for_user = zip(sorted_id, sorted_name, sorted_name_eng, sorted_image)
            
            print(sorted_id)
            print(sorted_name)
            print(sorted_image)
            print(len(sorted_id))
            print(len(sorted_name))
            print(len(sorted_name_eng))
            print(len(sorted_image))
            print(results_count)
       
            recommend_by_user = 0

        template = loader.get_template("search/searchByUserList.html")
        context = {
            "results_count": results_count,
            "sorted_id": sorted_id,
            "list_for_user": list_for_user,
            "user_id": user_id,
            "recommend_by_user" : recommend_by_user,
        }
        return HttpResponse(template.render(context, request))


class SearchByRankView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("search/searchByRank.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        template = loader.get_template("search/searchByRankList.html")

        rank_category = request.POST.get("rank_category")
        rank_qnty = request.POST.get("rank_qnty")

        # 조회수
        # if rank_category == "detailview" :
        #      list_by_rank = WinWine.objects.filter(wine_name__contains="0")

        # 구매수

        if rank_category == "purchaseqnty":
            purchaseqnty_joined = (
                WinPurchaseDetail.objects.select_related("sell")
                .values(
                    "sell__wine__wine_id",
                    "sell__wine__wine_name",
                    "sell__wine__wine_name_eng",
                    "sell__wine__wine_image",
                )
                .order_by("purchase_detail_id")
            )

            print(purchaseqnty_joined)
            print(purchaseqnty_joined.count())

            list_by_rank = (
                purchaseqnty_joined.values("sell__wine__wine_id")
                .annotate(
                    max_count=Count("sell__wine__wine_id"), w_i=F("sell__wine__wine_id")
                )
                .values(
                    "max_count",
                    "w_i",
                    "sell__wine__wine_id",
                    "sell__wine__wine_name",
                    "sell__wine__wine_name_eng",
                    "sell__wine__wine_image",
                )
                .order_by("-max_count")
            )

            print(list_by_rank)
        #
        # 판매 등록 수
        elif rank_category == "sellregist":
            sellregist_joined = (
                WinSell.objects.select_related("wine")
                .values(
                    "wine__wine_id",
                    "wine__wine_name",
                    "wine__wine_name_eng",
                    "wine__wine_image",
                )
                .order_by("sell_id")
            )

            print(sellregist_joined)
            print(sellregist_joined.count())

            list_by_rank = (
                sellregist_joined.values("wine__wine_id")
                .annotate(max_count=Count("wine__wine_id"), w_i=F("wine__wine_id"))
                .values(
                    "max_count",
                    "w_i",
                    "wine__wine_id",
                    "wine__wine_name",
                    "wine__wine_name_eng",
                    "wine__wine_image",
                )
                .order_by("-max_count")
            )

            print(list_by_rank.count())
            print(list_by_rank[1]["max_count"])
            print(list_by_rank[1]["wine__wine_name"])
            print(list_by_rank[1]["wine__wine_image"])

            for g in list_by_rank:
                print(g["max_count"])
                print(g["wine__wine_name"])
                print(g["wine__wine_name_eng"])
                print(g["wine__wine_image"])

        # # 리뷰 개수
        elif rank_category == "reviewqnty":
            reviewqnty_joined = (
                WinReview.objects.select_related("sell")
                .values(
                    "sell__wine__wine_id",
                    "sell__wine__wine_name",
                    "sell__wine__wine_name_eng",
                    "sell__wine__wine_image",
                )
                .order_by("review_id")
            )

            print(reviewqnty_joined)
            print(reviewqnty_joined.count())

            list_by_rank = (
                reviewqnty_joined.values("sell__wine__wine_id")
                .annotate(
                    max_count=Count("sell__wine__wine_id"), w_i=F("sell__wine__wine_id")
                )
                .values(
                    "max_count",
                    "w_i",
                    "sell__wine__wine_id",
                    "sell__wine__wine_name",
                    "sell__wine__wine_name_eng",
                    "sell__wine__wine_image",
                )
                .order_by("-max_count")
            )

            for g in list_by_rank:
                print(g["max_count"])
                print(g["sell__wine__wine_name"])
                print(g["sell__wine__wine_name_eng"])
                print(g["sell__wine__wine_image"])
        #
        # # 리뷰 평점
        elif rank_category == "reviewavg":
            reviewavg_joined = (
                WinReview.objects.select_related("sell")
                .values(
                    "review_score",
                    "sell__wine__wine_id",
                    "sell__wine__wine_name",
                    "sell__wine__wine_name_eng",
                    "sell__wine__wine_image",
                )
                .order_by("sell__wine__wine_id")
            )

            print(reviewavg_joined)
            print(reviewavg_joined.count())

            list_by_rank = (
                reviewavg_joined.values("sell__wine__wine_id")
                .annotate(avg=Avg("review_score"), w_i=F("sell__wine__wine_id"))
                .values(
                    "avg",
                    "w_i",
                    "sell__wine__wine_id",
                    "sell__wine__wine_name",
                    "sell__wine__wine_name_eng",
                    "sell__wine__wine_image",
                )
                .order_by("-avg")
            )

            for g in list_by_rank:
                print(g["avg"])
                print(g["sell__wine__wine_name"])
                print(g["sell__wine__wine_name_eng"])
                print(g["sell__wine__wine_image"])
        #
        # # 판매 평균 가격
        # elif rank_category == priceavg :
        #     list_by_rank = WinWine.objects.filter(wine_name__contains=search_word)
        #
        # # 구매 평균 가격
        # elif rank_category == priceavg :
        #     list_by_rank = WinWine.objects.filter(wine_name__contains=search_word)
        #

        list_count = list_by_rank.count()
        print(list_count)

        if int(rank_qnty) <= list_count:
            count = rank_qnty
        else:
            count = list_count
        count = int(count)

        list_by_rank = list_by_rank[:count]

        context = {
            "list_by_rank": list_by_rank,
            "count": count,
            "rank_category": rank_category,
            "rank_qnty": rank_qnty,
        }
        return HttpResponse(template.render(context, request))
