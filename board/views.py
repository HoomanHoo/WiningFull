from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views.generic.base import View
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from board.models import WinBoard, WinBoardImg, WinComment, WinBoardLike
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat
from _datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from django.core.paginator import Paginator

PAGE_SIZE = 20  # 한페이지에 표시할 게시물 개수
PAGE_BLOCK = 5  # 페이지 블록의 크기


# ListView는 게시판 페이지네이션과 게시글 목록을 구성하기 위해 필요한 데이터 계산
class ListView(View):
    def get(self, request):
        template = loader.get_template("board/list.html")
        count = WinBoard.objects.all().count()  # Board 모델이 저장된 게시글의 총 개수
        if count == 0:  # 게시글이 없는 경우
            context = {  # 템플릿에서도 사용하도록 변수 count 추가
                "count": count,
            }
        else:  # 게시글이 있는 경우
            pagenum = request.GET.get("pagenum")  # pagenum(현재 페이지 번호) 가져옴
            if not pagenum:  # pagenum(현재페이지번호)이 존재하지 않는 경우,
                pagenum = "1"  # 그때의 값을 1이라고 하자.
            pagenum = int(pagenum)  # pagenum:현재페이지번호     pagesize:페이지당 글개수
            start = (pagenum - 1) * int(PAGE_SIZE)  # (5-1)*10 + 1 = 41
            end = start + int(PAGE_SIZE)  # 41 + 10 - 1 = 50
            if end > count:  # end(끝인덱스)가 게시글 총 개수를 초과한다면...
                end = count  # end를 게시글 총개수로 바꾼다.

            search_query = request.GET.get("q")  # 검색어 가져오기
            if search_query:
                dtos = (
                    WinBoard.objects.annotate(comment_count=Count("wincomment"))
                    .filter(board_title__icontains=search_query)
                    .order_by("-board_reg_time")[start:end]
                )
                count = dtos.count()
            else:
                dtos = WinBoard.objects.annotate(
                    comment_count=Count("wincomment")
                ).order_by("-board_reg_time")[start:end]

            number = count - (pagenum - 1) * int(PAGE_SIZE)
            number = number - count - 1
            abs(number)

            paginator = Paginator(dtos, PAGE_SIZE)
            dtos = paginator.get_page(pagenum)

            startpage = pagenum // int(PAGE_BLOCK) * int(PAGE_BLOCK) + 1
            if pagenum % int(PAGE_BLOCK) == 0:
                startpage -= PAGE_BLOCK
            endpage = startpage + int(PAGE_BLOCK) - 1
            # startpage와 endpage를 계산하여 페이징 처리를 위한 페이지 번호의 범위를 구한다.

            pagecount = count // int(PAGE_SIZE)  # pagecount:총페이지 수

            if count % int(PAGE_SIZE) > 0:
                pagecount += 1
            if endpage > pagecount:  # endpage가 pagecount를 초과한다면
                endpage = pagecount  # endpage를 pagecount로 설정한다.
            pages = range(startpage, endpage + 1)

            context = {  # 필요한 변수들을 context내부에 추가해서 템플릿에서 사용할 수 있도록 한다.
                "count": count,
                "pagenum": pagenum,
                "dtos": dtos,
                "number": number,
                "startpage": startpage,
                "endpage": endpage,
                "pages": pages,
                "pageblock": PAGE_BLOCK,
                "pagecount": pagecount,
                "search_query": search_query,
                # "comment_count" : comment_count,
            }
        return HttpResponse(template.render(context, request))
        # 템플릿 렌더링한 결과를 context를 사용해서 Httpresponse로 return한다.


from django.core.files.storage import default_storage
from django.conf import settings


# 게시글 작성 기능담당. get요청-> 작성폼 보여줌   /  post요청-> 작성된 게시글 저장
class WriteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):  # dispatch메서드
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):  # get메서드
        template = loader.get_template("board/write.html")  # 해당 템플릿 로드
        num = request.GET.get("num")  # MultiValueDictKeyError 방지
        user_id = request.session.get("memid")
        # num :게시글번호
        # 템플릿에 전달한 변수를 context에 작성
        context = {
            "num": num,
            "user_id": user_id,
        }
        return HttpResponse(template.render(context, request))

    # post메서드
    def post(self, request):
        # user_id = request.POST.get("writer")
        board_title = request.POST.get("subject")
        board_content = request.POST.get("content")
        board_image = request.FILES.get("img")

        if not board_title or not board_content:
            # 필수 입력 필드가 누락된 경우 처리
            template = loader.get_template("board/write.html")
            context = {
                "num": request.POST.get("num"),
                "message": "모든 필드를 입력해주세요.",
            }
            return HttpResponse(template.render(context, request))

        dto = WinBoard(
            user_id=request.session.get("memid"),
            board_title=board_title,
            board_content=board_content,
            board_read_count=0,
            board_reg_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            board_ip=request.META.get("REMOTE_ADDR"),
            # board_like=0,
            # board_image=image_url,
        )
        dto.save()  # 생성된 객체를 DB에 저장

        if board_image:
            # 이미지가 업로드된 경우
            # 이미지를 파일로 저장
            image_path = default_storage.save("images/" + board_image.name, board_image)
            # 저장된 파일의 경로
            # image_url = settings.MEDIA_URL + image_path                                 # /media/images/
            image_url = "/" + image_path
            # WinBoardImg 모델에 저장
            win_board_img = WinBoardImg(board=dto, board_image=image_url)
            win_board_img.save()
        return redirect("board:list")  # boardlist url로 돌아감


class WriteCommentView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("board/writecomment.html")
        num = request.GET.get("board_id")  # MultiValueDictKeyError 방지
        user_id = request.session.get("memid")
        context = {
            "num": num,
            "user_id": user_id,
        }

        return HttpResponse(template.render(context, request))

    def post(self, request):
        board_id = request.POST.get("board_id")
        user_id = request.POST.get("writer")
        comment_content = request.POST.get("content")

        if not comment_content:
            # 필수 입력 필드가 누락된 경우 처리
            template = loader.get_template("board/writecomment.html")
            context = {
                "num": board_id,
                "message": "모든 필드를 입력해주세요.",
            }
            return HttpResponse(template.render(context, request))

        dtc = WinComment(
            # comment_id=request.POST["commenter"],
            board_id=board_id,
            user_id=user_id,
            comment_content=comment_content,
            comment_reg_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            content_ip=request.META.get("REMOTE_ADDR"),
        )
        dtc.save()

        return redirect("board:list")  # 리디렉션할 URL로 수정


@method_decorator(csrf_exempt, name="dispatch")
class UpdateCommentView(View):
    def post(self, request):
        comment_id = request.POST.get("comment_id")  # 수정할 댓글의 ID
        comment_content = request.POST.get("comment_content")  # 수정된 댓글 내용
        user_id = request.POST.get("user_id")  # 댓글 작성자의 ID

        # 댓글 ID와 내용이 모두 넘어왔는지 확인
        if not comment_id or not comment_content or not user_id:
            return JsonResponse({"success": False, "message": "모든 필드를 입력해주세요."})

        try:
            # DB에서 해당 댓글 가져오기
            comment = WinComment.objects.get(pk=comment_id)
        except WinComment.DoesNotExist:
            return JsonResponse({"success": False, "message": "해당 댓글을 찾을 수 없습니다."})

        # 댓글 작성자와 현재 로그인한 사용자가 같은지 검사

        if comment.user_id != user_id:
            return JsonResponse({"success": False, "message": "권한이 없습니다."}, status=403)

        # 댓글 내용 업데이트
        comment.comment_content = comment_content
        comment.save()

        # 수정된 댓글 내용을 응답으로 보내기
        return JsonResponse(
            {
                "success": True,
                "comment_id": comment.id,
                "comment_content": comment.comment_content,
                "comment_reg_time": comment.comment_reg_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "user_id": comment.user_id,
            }
        )


class DeleteCommentView(View):
    def delete(self, request, comment_id=None):
        dtc = get_object_or_404(WinComment, comment_id=comment_id)
        dtc.board_id = request.GET.get("board_id")
        pagenum = request.GET.get("pagenum")

        dtc.delete()

        return JsonResponse({"success": True})

    def post(self, request, comment_id=None):
        dtc = get_object_or_404(WinComment, comment_id=comment_id)
        dtc.board_id = request.POST.get("board_id")
        pagenum = request.POST.get("pagenum")

        dtc.delete()

        return JsonResponse({"success": True})


from django.utils import timezone
import json


class ContentView(View):
    def get(self, request):
        template = loader.get_template("board/content.html")
        num = request.GET.get("num")
        pagenum = request.GET.get("pagenum")
        number = request.GET.get("number")

        # 필수 매개변수가 없는 경우 기본값 설정
        if not num:
            num = 0
        else:
            num = int(num)

        dto = get_object_or_404(WinBoard, board_id=num)

        if dto.board_ip != request.META.get("REMOTE_ADDR"):
            dto.board_read_count += 1
            dto.save()

        dtcs = WinComment.objects.filter(board_id=num).values(
            "comment_id",
            "board_id",
            "user_id",
            "comment_content",
            "comment_reg_time",
            "content_ip",
        )

        dti = WinBoardImg.objects.filter(board=dto).first()
        image_url = dti.board_image.url if dti and dti.board_image else ""

        comment_count = WinComment.objects.filter(board_id=num).count()

        context = {
            "dto": dto,
            "dtcs": dtcs,
            "board_id": num,
            "pagenum": pagenum,
            "number": number,
            "image_url": image_url,
            "comment_count": comment_count,
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        board_id = request.POST.get("board_id")
        user_id = request.POST.get("writer")
        comment_content = request.POST.get("content")
        comment_id = request.POST.get("comment_id")  # 수정할 댓글의 ID

        if not board_id or not user_id or not comment_content:
            # 필수 입력 필드가 누락된 경우 처리
            template = loader.get_template("board/writecomment.html")
            context = {
                "num": board_id,
                "message": "모든 필드를 입력해주세요.",
            }
            return HttpResponse(template.render(context, request))

        # 댓글 수정을 위한 추가 로직
        if comment_id:
            dtc = get_object_or_404(WinComment, pk=comment_id)
            # 댓글 작성자와 현재 로그인한 사용자가 같은지 검사
            if dtc.user_id != user_id:
                return JsonResponse(
                    {"success": False, "message": "권한이 없습니다."}, status=403
                )

            dtc.comment_content = comment_content
            dtc.save()

            # JSON 응답 생성
            return JsonResponse({"success": True, "message": "댓글이 수정되었습니다."})
        else:
            dtc = WinComment(
                board_id=board_id,
                user_id=user_id,
                comment_content=comment_content,
                comment_reg_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                content_ip=request.META.get("REMOTE_ADDR"),
            )
            dtc.save()

        # JSON 응답 생성
        return JsonResponse({"success": True, "dtc": dtc})


from django.shortcuts import reverse
from django.utils.http import urlencode


class DeleteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Delete confirmation page
        # template = loader.get_template("board/delete.html")
        num = request.GET["num"]
        pagenum = request.GET["pagenum"]
        dto = WinBoard.objects.get(board_id=num)

        if dto.user_id == request.session.get("memid"):
            dto.delete()

        url = reverse("board:list") + "?" + urlencode({"pagenum": pagenum})
        return redirect(url)


import os
from django.core.files.storage import default_storage


class UpdateView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        num = request.GET["num"]
        template = loader.get_template("board/updatepro.html")
        dto = WinBoard.objects.get(board_id=num)

        dti = WinBoardImg.objects.filter(board=dto).first()
        image_url = dti.board_image.url if dti and dti.board_image else ""
        image_name = dti.board_image.name if dti and dti.board_image else ""

        context = {
            "dto": dto,
            "num": request.GET["num"],
            "pagenum": request.GET["pagenum"],
            "image_url": image_url,
            "image_name": image_name,
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        num = request.POST["num"]
        pagenum = request.POST["pagenum"]
        dto = WinBoard.objects.get(board_id=num)

        dto.board_title = request.POST["subject"]
        dto.board_content = request.POST["content"]

        # 이미지 업로드 처리
        if "img" in request.FILES:
            dti = WinBoardImg.objects.filter(board=dto).first()
            if not dti:
                dti = WinBoardImg()
                dti.board = dto
            dti.board_image = request.FILES["img"]
            dti.save()

        # 이미지 삭제 처리
        delete_image_id = request.POST.get("delete_image_id")
        if delete_image_id:
            try:
                # 이미지 파일을 삭제하기 위해 파일 경로를 구합니다.
                dti = WinBoardImg.objects.get(pk=delete_image_id)
                image_path = dti.board_image.path if dti and dti.board_image else None

                if image_path:
                    # 이미지 파일이 존재하면 파일을 삭제합니다.
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    dti.delete()  # 해당 이미지 객체도 삭제합니다.

            except Exception as e:
                print(f"Error deleting image: {e}")

        dto.save()
        return redirect("board:list")


import string


class UpdateProView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, num):
        dto = WinBoard.objects.get(board_id=num)
        dti = WinBoardImg.objects.filter(board=dto).first()
        image_name = dti.board_image.name if dti and dti.board_image else ""

        # 캐시 무효화를 위해 랜덤한 문자열을 생성하여 cache_buster로 전달합니다.
        cache_buster = "".join(random.choice(string.ascii_lowercase) for _ in range(10))

        context = {
            "dto": dto,
            "dti": dti,
            "image_name": image_name,
            "cache_buster": cache_buster,
        }
        return render(request, "updatepro.html", context)

    def post(self, request):
        num = request.POST["num"]
        dto = WinBoard.objects.get(board_id=num)
        dto.board_title = request.POST["subject"]
        dto.board_content = request.POST["content"]

        # 이미지 업로드 처리
        if "img" in request.FILES:
            dti = WinBoardImg.objects.filter(board=dto).first()
            if not dti:
                dti = WinBoardImg()
                dti.board = dto
            dti.board_image = request.FILES["img"]
            dti.save()

        # 이미지 삭제 처리
        delete_image_id = request.POST.get("delete_image_id")
        if delete_image_id:
            try:
                # 이미지 파일을 삭제하기 위해 파일 경로를 구합니다.
                delete_image_path = os.path.join(settings.MEDIA_ROOT, delete_image_id)
                # 이미지 파일이 존재하면 파일을 삭제합니다.
                if os.path.exists(delete_image_path):
                    os.remove(delete_image_path)
                else:
                    print(f"Image not found: {delete_image_path}")
            except Exception as e:
                print(f"Error deleting image: {e}")

            # 해당 게시글에 연결된 이미지를 삭제합니다.
            WinBoardImg.objects.filter(board=dto, board_image=delete_image_id).delete()
            print("첨부된 이미지가 삭제되었습니다.")
        else:
            print("이미지가 수정되지 않아서, 게시글만 수정됩니다.")

        request.session["modified_post_id"] = dto.board_id
        dto.save()
        return redirect("board:list")


class RecentModifiedPostsView(View):
    def get(self, request):
        # 최근 수정된 댓글 정보를 가져옵니다.
        recent_posts = WinBoard.objects.filter(modified=True)
        data = [post.id for post in recent_posts]
        return JsonResponse({"modified_posts": data})


class DeleteImageView(View):
    def post(self, request):
        image_id = request.POST.get("delete_image_id")

        if not image_id:
            return JsonResponse(
                {"success": False, "message": "이미지 ID가 필요합니다."}, status=400
            )

        try:
            # 이미지 파일을 삭제하기 위해 파일 경로를 구합니다.
            dti = WinBoardImg.objects.get(pk=image_id)
            image_path = dti.board_image.path if dti and dti.board_image else None

            if not image_path:
                return JsonResponse(
                    {"success": False, "message": "삭제할 이미지를 찾을 수 없습니다."}, status=404
                )

            # 이미지 파일이 존재하면 파일을 삭제합니다.
            if os.path.exists(image_path):
                os.remove(image_path)
                dti.delete()  # 해당 이미지 객체도 삭제합니다.
            else:
                return JsonResponse(
                    {"success": False, "message": "삭제할 이미지를 찾을 수 없습니다."}, status=404
                )

            return JsonResponse({"success": True, "message": "이미지가 성공적으로 삭제되었습니다."})
        except Exception as e:
            print(f"Error deleting image: {e}")
            return JsonResponse(
                {"success": False, "message": "이미지 삭제 중 오류가 발생했습니다."}, status=500
            )


import time
import random


class UploadImageView(View):
    @staticmethod
    def generate_unique_id():
        timestamp = int(time.time() * 1000)  # 현재 시간을 밀리초 단위로 변환
        unique_id = (
            f"{timestamp}-{random.randint(1000, 9999)}"  # 현재 시간과 랜덤한 숫자를 조합하여 고유한 ID 생성
        )
        return unique_id

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("board/uploadimage.html")
        num = request.GET.get("board_id")

        context = {
            "num": num,
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        board_id = request.POST.get("board_id")
        board_image = request.FILES["img"]
        board_img_id = self.generate_unique_id()

        dti = WinBoardImg(
            board_img_id=board_img_id,
            board_id=board_id,
            board_image=board_image,
        )
        dti.save()

        return redirect("board:list")
