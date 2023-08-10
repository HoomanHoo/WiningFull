# from django.shortcuts import render
from django.views.generic.base import View

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.http.response import HttpResponse
from detail.models import WinWine, WinWineRegion, WinDetailView, WinDetailViewN
from _datetime import datetime
from django.utils.dateformat import DateFormat
from detail.datapair.datapair import get_pair, kind_pair, food_pair
from search.functions.functions import random_generate


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_client_ip_psuedo(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class WineDetailInfoView(View):
    def get(self, request):
        template = loader.get_template("detail/wineDetail.html")
        wine_id = request.GET["wine_id"]
        wine_info = WinWine.objects.get(wine_id=wine_id)
        region = WinWineRegion.objects.get(wine_region_id=wine_info.wine_region_id)
        det_kind = get_pair(kind_pair, wine_info.wine_sort)
        det_food = get_pair(food_pair, wine_info.wine_food)

        get_wines = WinWine.objects.all()
        get_qnty = get_wines.count()
        print(get_qnty)
        get_wine_id = get_wines.only("wine_id", "wine_image")
        print(get_wine_id)
        print(get_wine_id[0].wine_image)
        random_wine_id = random_generate(list(get_wine_id), 5)
        random_list = []

        for i in range(len(random_wine_id)):
            random_list.append(random_wine_id[i].wine_id)
        print(random_list)
        recommend_list = get_wines.only("wine_id", "wine_image").filter(
            wine_id__in=random_list
        )
        print(recommend_list[0].wine_id)
        print(recommend_list[1].wine_id)
        print(recommend_list[2].wine_id)
        print(recommend_list[3].wine_id)
        print(recommend_list[4].wine_id)

        if request.session.get("memid"):
            detail_rec = WinDetailView(
                user_id=request.session.get("memid"),
                wine_id=wine_id,
                detail_view_time=DateFormat(datetime.now()).format("Y-m-d h:i:s"),
            )

            detail_rec.save()

        else:
            detail_n_rec = WinDetailViewN(
                wine_id=wine_id,
                detail_view_n_time=DateFormat(datetime.now()).format("Y-m-d h:i:s"),
            )
            detail_n_rec.save()

        print(wine_info.wine_image)

        # 사용자 상세 보기 기록 남기기
        context = {
            "wine_info": wine_info,
            "region": region,
            "det_kind": det_kind,
            "det_food": det_food,
            "recommend_list": recommend_list,
        }
        return HttpResponse(template.render(context, request))
