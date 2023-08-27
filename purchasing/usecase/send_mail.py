import asyncio
import smtplib
from email.mime.text import MIMEText
import time
from Wining import settings


def send_charge_email(user_name: str, user_email: str, charge_point: int, charge_time):
    user_subject = user_name + "님의 포인트 충전 내역입니다."
    user_message = (
        user_name
        + "님의 포인트 충전 내역입니다. \n"
        + str(charge_point)
        + "원 \n"
        + "충전 일시: "
        + str(charge_time)
    )

    smtp = smtplib.SMTP("smtp.naver.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWD)
    msg = MIMEText(user_message)
    msg["From"] = settings.EMAIL_HOST_USER
    msg["Subject"] = user_subject
    msg["To"] = str(user_email)
    smtp.sendmail(settings.EMAIL_HOST_USER, str(user_email), msg.as_string())
    smtp.close()


async def send_purchase_email(
    user_name: str,
    user_email: str,
    purchase_info_list: list,
):
    mail_task = asyncio.create_task(
        async_send_purchase_email(
            user_name=user_name,
            user_email=user_email,
            purchase_info_list=purchase_info_list,
        )
    )
    await asyncio.gather(mail_task)


async def async_send_purchase_email(  # 메일 하나를 보내는데 0.3초의 딜레이가 발생하기 때문에 빠른 페이지 전환을 위해 비동기 함수 사용
    user_name: str,
    user_email: str,
    purchase_info_list: list,
):
    store_email_list = []
    wine_name_list = {}
    store_name_list = {}
    receive_code_list = {}
    purchase_det_number_list = {}
    purchase_det_price_list = {}
    store_address_list = {}

    customer_message = user_name + "님의 결제 내역입니다.\n"
    start = time.time()

    for purchase_info in purchase_info_list:
        wine_name = purchase_info["purchase_detail_id__sell__wine__wine_name"]
        purchase_det_number = purchase_info["purchase_detail_id__purchase_det_number"]
        purchase_det_price = purchase_info["purchase_detail_id__purchase_det_price"]
        store_name = purchase_info["purchase_detail_id__sell__store__store_name"]
        store_address = purchase_info["purchase_detail_id__sell__store__store_address"]
        store_email = purchase_info["purchase_detail_id__sell__store__store_email"]
        receive_code = purchase_info["receive_code"]

        customer_message += (
            "\n"
            + str(store_name)
            + " "
            + str(store_address)
            + " "
            + str(wine_name)
            + " "
            + str(purchase_det_number)
            + "개 "
            + str(purchase_det_price)
            + "원  수령코드: "
            + str(receive_code)
            + "\n"
        )

        if store_email not in store_email_list:
            store_email_list.append(store_email)
            wine_name_list[store_email] = [wine_name]
            store_name_list[store_email] = [store_name]
            purchase_det_number_list[store_email] = [purchase_det_number]
            receive_code_list[store_email] = [receive_code]
            purchase_det_price_list[store_email] = [purchase_det_price]
            store_address_list[store_email] = [store_address]

        elif store_email in store_email_list:
            wine_name_list[store_email].append(wine_name)
            purchase_det_number_list[store_email].append(purchase_det_number)
            receive_code_list[store_email].append(receive_code)
            purchase_det_price_list[store_email].append(purchase_det_price)
            store_address_list[store_email].append(store_address)

    subject = user_name + "님 Wining 결제 내역입니다"
    to = str(user_email)
    from_email = str(settings.EMAIL_HOST_USER)
    message = customer_message

    smtp = smtplib.SMTP("smtp.naver.com", 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWD)

    msg = MIMEText(message)
    msg["From"] = settings.EMAIL_HOST_USER
    msg["Subject"] = subject
    msg["To"] = to
    smtp.sendmail(from_email, str(user_email), msg.as_string())

    await asyncio.sleep(0.3)
    end = time.time()
    print("async for 함수 전 까지의 실행 시간", end - start)
    start2 = time.time()
    async for i in SendMail(
        user_name,
        store_email_list,
        wine_name_list,
        store_name_list,
        purchase_det_number_list,
        purchase_det_price_list,
        smtp,
    ):
        print(i)

    smtp.quit()
    end2 = time.time()
    print("async for 함수 있는 구간의 실행 시간", end2 - start2)


class SendMail:
    def __init__(
        self,
        user_name,
        store_email_list,
        wine_name_list,
        store_name_list,
        purchase_det_number_list,
        purchase_det_price_list,
        smtp,
    ):
        self.user_name = user_name
        self.store_email_list = store_email_list
        self.wine_name_list = wine_name_list
        self.store_name_list = store_name_list
        self.purchase_det_number_list = purchase_det_number_list
        self.purchase_det_price_list = purchase_det_price_list
        self.smtp = smtp

    def __aiter__(self):
        return self

    async def __anext__(self):
        i = 0
        if i < len(self.store_email_list):
            raise StopAsyncIteration

        else:
            store_email = self.store_email_list[i]
            store_message = (
                str(self.store_name_list[store_email][0])
                + "님 "
                + self.user_name
                + "님의 주문 내역 입니다\n"
            )
            for idx, wine_name in enumerate(self.wine_name_list[store_email]):
                store_message += (
                    "\n"
                    + str(wine_name)
                    + " "
                    + str(self.purchase_det_number_list[store_email][idx])
                    + "개 "
                    + str(self.purchase_det_price_list[store_email][idx])
                    + "원 "
                    + "\n"
                )
            subject = (
                str(self.store_name_list[store_email][0])
                + "님 "
                + self.user_name
                + "님의 주문 내역 입니다"
            )
            to = str(store_email)
            from_email = str(settings.EMAIL_HOST_USER)
            message = store_message

            msg = MIMEText(message)
            msg["From"] = settings.EMAIL_HOST_USER
            msg["Subject"] = subject
            msg["To"] = to
            await asyncio.sleep(0.3)
            self.smtp.sendmail(from_email, str(store_email), msg.as_string())

            return i


# def s_send_purchase_email(
#     user_name: str,
#     user_email: str,
#     purchase_info_list: list,
# ):
#     sync_send_purchase_email(
#         user_name=user_name,
#         user_email=user_email,
#         purchase_info_list=purchase_info_list,
#     )


# def sync_send_purchase_email(  # 메일 하나를 보내는데 0.3초의 딜레이가 발생하기 때문에 빠른 페이지 전환을 위해 비동기 함수 사용
#     user_name: str,
#     user_email: str,
#     purchase_info_list: list,
# ):
#     store_email_list = []
#     wine_name_list = {}
#     store_name_list = {}
#     receive_code_list = {}
#     purchase_det_number_list = {}
#     purchase_det_price_list = {}
#     store_address_list = {}

#     customer_message = user_name + "님의 결제 내역입니다.\n"
#     start3 = time.time()

#     for purchase_info in purchase_info_list:
#         wine_name = purchase_info["purchase_detail_id__sell__wine__wine_name"]
#         purchase_det_number = purchase_info["purchase_detail_id__purchase_det_number"]
#         purchase_det_price = purchase_info["purchase_detail_id__purchase_det_price"]
#         store_name = purchase_info["purchase_detail_id__sell__store__store_name"]
#         store_address = purchase_info["purchase_detail_id__sell__store__store_address"]
#         store_email = purchase_info["purchase_detail_id__sell__store__store_email"]
#         receive_code = purchase_info["receive_code"]

#         customer_message += (
#             "\n"
#             + str(store_name)
#             + " "
#             + str(store_address)
#             + " "
#             + str(wine_name)
#             + " "
#             + str(purchase_det_number)
#             + "개 "
#             + str(purchase_det_price)
#             + "원  수령코드: "
#             + str(receive_code)
#             + "\n"
#         )

#         if store_email not in store_email_list:
#             store_email_list.append(store_email)
#             wine_name_list[store_email] = [wine_name]
#             store_name_list[store_email] = [store_name]
#             purchase_det_number_list[store_email] = [purchase_det_number]
#             receive_code_list[store_email] = [receive_code]
#             purchase_det_price_list[store_email] = [purchase_det_price]
#             store_address_list[store_email] = [store_address]

#         elif store_email in store_email_list:
#             wine_name_list[store_email].append(wine_name)
#             purchase_det_number_list[store_email].append(purchase_det_number)
#             receive_code_list[store_email].append(receive_code)
#             purchase_det_price_list[store_email].append(purchase_det_price)
#             store_address_list[store_email].append(store_address)

#     subject = user_name + "님 Wining 결제 내역입니다"
#     to = str(user_email)
#     from_email = str(settings.EMAIL_HOST_USER)
#     message = customer_message

#     smtp = smtplib.SMTP("smtp.naver.com", 587)
#     smtp.ehlo()  # say Hello
#     smtp.starttls()  # TLS 사용시 필요
#     smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWD)

#     msg = MIMEText(message)
#     msg["From"] = settings.EMAIL_HOST_USER
#     msg["Subject"] = subject
#     msg["To"] = to
#     smtp.sendmail(from_email, str(user_email), msg.as_string())

#     time.sleep(0.3)
#     end3 = time.time()
#     print("동기함수 for문 전까지의 실행시간", end3 - start3)

#     start4 = time.time()
#     for store_email in store_email_list:
#         store_message = (
#             str(store_name_list[store_email][0]) + "님 " + user_name + "님의 주문 내역 입니다\n"
#         )
#         for idx, wine_name in enumerate(wine_name_list[store_email]):
#             store_message += (
#                 "\n"
#                 + str(wine_name)
#                 + " "
#                 + str(purchase_det_number_list[store_email][idx])
#                 + "개 "
#                 + str(purchase_det_price_list[store_email][idx])
#                 + "원 "
#                 + "\n"
#             )
#         subject = (
#             str(store_name_list[store_email][0]) + "님 " + user_name + "님의 주문 내역 입니다"
#         )
#         to = str(store_email)
#         from_email = str(settings.EMAIL_HOST_USER)
#         message = store_message

#         msg = MIMEText(message)
#         msg["From"] = settings.EMAIL_HOST_USER
#         msg["Subject"] = subject
#         msg["To"] = to
#         smtp.sendmail(from_email, str(store_email), msg.as_string())
#         time.sleep(0.3)

#     smtp.quit()
#     end4 = time.time()
#     print("동기함수 for문 있는 구간의 실행 시간", end4 - start4)


# django mail은 smtp 단에서 인증 오류가 발생하여 사용할 수 없음
# result = EmailMessage(
#     subject=subject,
#     body=message,
#     from_email=from_email,
#     to=to,
#     connection=get_connection(settings.EMAIL_BACKEND, fail_silently=False),
# )
# result.send()

# seller_message = ""
# for store_email in store_email_list:
#     store_email = str(store_email)
#     store_name = store_name_list[store_email]
#     wine_name = wine_name_list[store_email]
#     purchase_det_number = purchase_det_number_list[store_email]
#     receive_code = receive_code_list[store_email]

#     seller_messeage += (
#         store_name_list[store_email]
#         + " "
#         + wine_name_list[store_email]
#         + " "
#         + purchase_det_number_list[store_email]
#         + "개 "
#         + purchase_det_price_list[store_email]
#         + "원  수령코드: "
#         + receive_code_list[store_email]
#     )

# subject = user_name + "님 Wining 결제 내역입니다"
# to = [user_email]
# from_email = settings.EMAIL_HOST_USER
# message = customer_messeage
# EmailMessage(subject=subject, body=message, from_email=from_email, to=to).send()
