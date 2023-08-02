from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from user.models import WinUser, WinUserGrade, WinUserFavorite, WinReview, WinPointHis
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateformat import DateFormat
from datetime import datetime
from board.models import WinBoard, WinComment, WinBoardImg
from store.models import WinSell
from purchasing.models import WinPurchase, WinPurchaseDetail, WinCart, WinReceiveCode,\
    WinCartDetail
from detail.models import WinDetailView
from django.contrib.messages.context_processors import messages
from django.urls.base import reverse
from django.db.models import F
from django.core.files.storage import default_storage


class LoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("user/login.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = request.POST["user_id"]
        user_passwd = request.POST["user_passwd"]

        try:
            dto = WinUser.objects.get(user_id=user_id)
            user_grade = dto.user_grade.user_grade

            if user_passwd == dto.user_passwd:
                if user_grade != -1:
                    request.session["memid"] = user_id
                    return redirect("myPage")

                else:
                    message = "탈퇴한 회원입니다"

            else:
                message = "입력하신 비밀번호가 다릅니다"
        except ObjectDoesNotExist:
            message = "입력하신 아이디가 없습니다"

        template = loader.get_template("user/login.html")
        context = {
            "message": message,
        }

        return HttpResponse(template.render(context, request))


class LogoutView(View):
    def get(self, request):
        del request.session["memid"]
        return redirect("login")


# return redirect("user/login.html")


class InputUserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("user/inputUser.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_point = 0
        # default_grade = 1

        dto = WinUser(
            user_id = request.POST["user_id"],
            user_grade = WinUserGrade.objects.get(user_grade=1),
            user_passwd = request.POST["user_passwd"],
            user_name = request.POST["user_name"],
            user_email = request.POST["user_email"],
            user_tel = request.POST["user_tel"],
            user_reg_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_point = user_point,
        )
        dto.save()

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
        fdto.save()

        # message = "회원가입에 성공했습니다"
        # alert_script = f'<script>alert("{message}");</script>'

        return redirect("login")


class InputStoreView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("user/inputStore.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_point = 0
        user_id = request.POST["user_id"]
        # user_input =
        WinUser(
            user_id=user_id,
            user_grade=WinUserGrade.objects.get(user_grade=1),
            user_passwd=request.POST["user_passwd"],
            user_name=request.POST["user_name"],
            user_email=request.POST["user_email"],
            user_tel=request.POST["user_tel"],
            user_reg_date=DateFormat(datetime.now()).format("Y-m-d h:i:s"),
            user_point=user_point,
        ).save()
        request.session["temp_id"] = user_id

        # return redirect("/store/store-registration")
        return redirect("storeRegistration")

        # 로그인도 회원가입도 되지 않았을 때 가입 시 입력 아이디를 세션에 저장한다.
        # redirect로 이동한다. context에 id를 넣어 보내면 주소가 이동하지 않고 redirect 를 쓰면 id를 보낼 수 없다.
        # 그래서 로그인하지 않았지만 회원가입 시 임시로 입력한 id를 세션에 저장하고 store 에서 꺼내 쓴다.


class ConfirmIdView(View):
    def get(self, request):
        template = loader.get_template("user/confirmId.html")
        user_id = request.GET["user_id"]
        result = 0

        try:
            WinUser.objects.get(user_id=user_id)
            result = 1
        except ObjectDoesNotExist:
            result = 0
        context = {"result": result, "user_id": user_id}

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

        dto = WinUser.objects.get(user_id=user_id)

        if user_passwd == dto.user_passwd:
            w_user_grade = WinUserGrade.objects.get(user_grade=-1)
            dto.user_grade = w_user_grade
            dto.save()

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
        dto = WinUser.objects.get(user_id=user_id)
        print(dto.user_grade_id)
        if (dto.user_grade_id == 1) : 
            try:
                fdto = WinUserFavorite.objects.get(user_id=user_id)
            except WinUserFavorite.DoesNotExist:
                fdto = None
            context = {"user_id": user_id, "dto": dto, "fdto": fdto}
        else: 
            context = {"user_id": user_id, "dto": dto}

        return HttpResponse(template.render(context, request))

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
            fdto.fav_first_priority=request.POST["fav_first"]
            fdto.fav_second_priority=request.POST["fav_second"]
            fdto.fav_third_priority=request.POST["fav_third"]

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
            fdto.fav_first_priority=request.POST["fav_first"]
            fdto.fav_second_priority=request.POST["fav_second"]
            fdto.fav_third_priority=request.POST["fav_third"]

            fdto.save()

        return redirect("myPage")


class MyPageView(View):
    def get(self, request):
        template = loader.get_template("user/myPage.html")
        memid = request.session.get("memid")
        dto = WinUser.objects.get(user_id=memid)
        purchase_c = WinPurchase.objects.filter(user_id=memid).count()
        review_c = WinReview.objects.filter(user_id=memid).count()
        cart_c = WinCartDetail.objects.select_related("cart").filter(cart__user_id=memid).count()
        detail_v = WinDetailView.objects.filter(user_id=memid).order_by(
            "-detail_view_time"
        )[:6].select_related("wine")
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
            user = WinUser.objects.get(user_id=user_id),
            sell_id = sell_id,
            review_content = request.POST["content"],
            review_score = request.POST["rating"],
            review_reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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

                dtos.append(
                    {
                        "wine_name": wine_name,
                        "wine_name_eng": wine_name_eng,
                        "wine_image": wine_image,
                        "purchase_price": purchase_price,
                        "purchase_number": purchase_number,
                        "purchase_time": purchase_time,
                        "sell_id": sell_id,
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
            

            
        context = {"dtos_and_images": dtos_and_images,
                   "user_id" : user_id,
                  }
        
        
        return HttpResponse(template.render(context, request))


class MyCommentView(View):
    def get(self, request):
        template = loader.get_template("user/myComment.html")
        user_id = request.session.get("memid")
        dtos = WinComment.objects.filter(user_id=user_id).order_by("-comment_reg_time")

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
            user = WinUser.objects.get(user_id=dto.user_id),
            point_reg = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            point_add = chargepoint,
        )

        pdto.save()

        return redirect("myPage")


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
                "store_name",
                "wine_name",
                "receive_code",
            )
        )

        list_length = dtos.count()
        if int(list_length) % int(show_length):
            pages = int(list_length) // int(show_length)
        else:
            pages = int(list_length) // int(show_length) + 1
        pdtos = dtos[start:end]
        pages_list = [i + 1 for i in range(pages)]

        context = {"pdtos": pdtos, "pages_list": pages_list}
        return HttpResponse(template.render(context, request))
